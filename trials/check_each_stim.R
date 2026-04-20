# ============================================================
# check_each_stim.R
# Single script: reads all trial CSVs and produces summary outputs
# ============================================================

library(dplyr)
library(tidyr)
library(purrr)
library(stringr)

root_dir <- "trial_lists_768"

files <- list.files(
  root_dir,
  pattern = "^order_[0-9]{3}\\.csv$",
  recursive = TRUE,
  full.names = TRUE
)

if (length(files) == 0) {
  stop("No order_###.csv files found under: ", root_dir)
}

cat("Files found:", length(files), "\n")

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------

all_trials <- map_dfr(files, function(f) {
  read.csv(f, stringsAsFactors = FALSE) %>%
    mutate(source_file = basename(f))
})

all_trials <- all_trials %>%
  mutate(
    familiarization_time = as.integer(familiarization_time),
    complexity_condition = as.character(complexity_condition),
    familiar_stimulus_item = as.character(familiar_stimulus_item),
    novel_stimulus_item = as.character(novel_stimulus_item)
  )

cat("Total rows:", nrow(all_trials), "\n")

# ------------------------------------------------------------
# Long format
# ------------------------------------------------------------

long_trials <- bind_rows(
  all_trials %>%
    transmute(
      stimulus_item = familiar_stimulus_item,
      role = "familiar",
      complexity = complexity_condition,
      time_s = familiarization_time
    ),
  all_trials %>%
    transmute(
      stimulus_item = novel_stimulus_item,
      role = "novel",
      complexity = complexity_condition,
      time_s = familiarization_time
    )
) %>%
  mutate(
    role = factor(role, levels = c("familiar", "novel")),
    complexity = factor(complexity, levels = c("simple", "complex")),
    time_s = as.integer(time_s)
  )

# ------------------------------------------------------------
# Per-stimulus summary
# ------------------------------------------------------------

stimulus_summary <- long_trials %>%
  group_by(stimulus_item) %>%
  summarise(
    familiar_count = sum(role == "familiar"),
    novel_count = sum(role == "novel"),
    simple_count = sum(complexity == "simple"),
    complex_count = sum(complexity == "complex"),
    time_5_count = sum(time_s == 5),
    time_10_count = sum(time_s == 10),
    time_15_count = sum(time_s == 15),
    .groups = "drop"
  ) %>%
  arrange(stimulus_item)

# ------------------------------------------------------------
# Helper for breakdown tables
# ------------------------------------------------------------

make_summary <- function(data, role_val, comp_val, prefix) {
  data %>%
    filter(role == role_val, complexity == comp_val) %>%
    group_by(stimulus_item, time_s) %>%
    summarise(n = n(), .groups = "drop") %>%
    complete(
      stimulus_item,
      time_s = c(5, 10, 15),
      fill = list(n = 0)
    ) %>%
    pivot_wider(
      names_from = time_s,
      values_from = n,
      names_prefix = prefix
    )
}

# ------------------------------------------------------------
# Full breakdown
# ------------------------------------------------------------

simple_familiar <- make_summary(long_trials, "familiar", "simple", "simple_familiar_time_")
complex_familiar <- make_summary(long_trials, "familiar", "complex", "complex_familiar_time_")
simple_novel <- make_summary(long_trials, "novel", "simple", "simple_novel_time_")
complex_novel <- make_summary(long_trials, "novel", "complex", "complex_novel_time_")

combined_summary <- stimulus_summary %>%
  left_join(simple_familiar, by = "stimulus_item") %>%
  left_join(complex_familiar, by = "stimulus_item") %>%
  left_join(simple_novel, by = "stimulus_item") %>%
  left_join(complex_novel, by = "stimulus_item") %>%
  arrange(stimulus_item)

# ------------------------------------------------------------
# Save outputs
# ------------------------------------------------------------

write.csv(
  stimulus_summary,
  file.path(root_dir, "stimulus_summary_by_item.csv"),
  row.names = FALSE
)

write.csv(
  combined_summary,
  file.path(root_dir, "combined_stimulus_summary_by_item.csv"),
  row.names = FALSE
)

cat("Done. Files written to:", root_dir, "\n")
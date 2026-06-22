# ============================================================
# generate_trial_lists.R
# Full 768-order generator + checker
# 48 labs x 16 CSVs per lab = 768 total CSVs
# Each CSV contains a full 12-trial structure.
# Complexity is strictly balanced by stimulus type and time.
# Location order is a seeded balanced shuffle with 6 left / 6 right.
# ============================================================

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

capitalize_first <- function(x) {
  paste0(toupper(substr(x, 1, 1)), substr(x, 2, nchar(x)))
}

split_and_reverse <- function(lst) {
  if (length(lst) %% 2 != 0) {
    stop("List length must be even to split evenly in half.")
  }
  mid <- length(lst) / 2
  c(rev(lst[1:mid]), rev(lst[(mid + 1):length(lst)]))
}

handle_reverse_ordering <- function(trial_list_element, reverse_order_block, reverse_order_list) {
  if (reverse_order_block == "base_rev") {
    if (reverse_order_list == "rev") {
      return(rev(split_and_reverse(trial_list_element)))
    } else {
      return(split_and_reverse(trial_list_element))
    }
  } else {
    if (reverse_order_list == "rev") {
      return(rev(trial_list_element))
    } else {
      return(trial_list_element)
    }
  }
}

invert_complexity <- function(comp_vec) {
  ifelse(comp_vec == "simple", "complex", "simple")
}

count_or_zero <- function(tab, key) {
  if (key %in% names(tab)) as.integer(tab[[key]]) else 0L
}

make_balanced_location_order <- function(seed) {
  set.seed(seed)
  sample(c(rep("left", 6), rep("right", 6)))
}

# Strict complexity assignment:
# For each stimulus type (fribble / fractal) and each time (5/10/15),
# choose exactly one simple and one complex among the two rows in that stratum.
make_strict_complexity <- function(row_type_vec, time_vec, seed) {
  set.seed(seed)
  
  comp <- rep(NA_character_, length(time_vec))
  
  for (stim_type in c("fribble", "fractal")) {
    for (t in c(5, 10, 15)) {
      idx <- which(row_type_vec == stim_type & time_vec == t)
      
      if (length(idx) != 2) {
        stop(paste0(
          "Expected exactly 2 rows for ", stim_type, " at time ", t,
          ", but found ", length(idx), "."
        ))
      }
      
      simple_idx <- sample(idx, 1)
      comp[simple_idx] <- "simple"
      comp[setdiff(idx, simple_idx)] <- "complex"
    }
  }
  
  if (sum(comp == "simple") != 6 || sum(comp == "complex") != 6) {
    stop("Complexity assignment is not globally balanced 6 simple / 6 complex.")
  }
  
  comp
}

# ------------------------------------------------------------
# Global stimulus dictionaries
# ------------------------------------------------------------

fribble_dict <- list(
  set_1 = list(
    c("Tripod", "Diamond"),
    c("SimsDiamond", "Cylinder"),
    c("Pyramid", "Bowtie"),
    c("Pacman", "Arrow"),
    c("Crinkle", "Pumpkin"),
    c("Bowl", "Gumdrop")
  ),
  set_2 = list(
    c("Pacman", "Cylinder"),
    c("Bowtie", "Arrow"),
    c("Tripod", "Bowl"),
    c("Crinkle", "Diamond"),
    c("Pyramid", "Gumdrop"),
    c("SimsDiamond", "Pumpkin")
  )
)

fractal_dict <- list(
  set_1 = list(
    c("pair1_a", "pair1_b"),
    c("pair2_a", "pair2_b"),
    c("pair3_a", "pair3_b"),
    c("pair4_a", "pair4_b"),
    c("pair5_a", "pair5_b"),
    c("pair6_a", "pair6_b")
  )
)

familiarization_time_pairs <- list(
  list(c(5, 10, 15), c(10, 15, 5)),
  list(c(5, 15, 10), c(15, 10, 5)),
  list(c(10, 5, 15), c(15, 5, 10))
)

# ------------------------------------------------------------
# Build one full 12-trial CSV
# ------------------------------------------------------------

build_trial_df <- function(
    order_id,
    lab_number,
    base_lab_id,
    complexity_polarity,
    fribble_set,
    reverse_order_block,
    reverse_order_list,
    time_pair_group,
    stimulus_type_order,
    familiar_role,
    location_shuffle_group,
    time_order_index,
    rel_image_path = "stimuli/images/",
    img_ext = ".png",
    test_time = 5) {
  
  trial_num <- 12
  fractal_set <- "set_1"
  
  # Base time pattern for this list.
  cur_familiarization_time_set <- familiarization_time_pairs[[time_pair_group]][[time_order_index]]
  fam_time_1 <- cur_familiarization_time_set[1]
  fam_time_2 <- cur_familiarization_time_set[2]
  fam_time_3 <- cur_familiarization_time_set[3]
  
  fam_time_list <- c(
    fam_time_2, fam_time_3, fam_time_1,
    fam_time_1, fam_time_3, fam_time_2,
    fam_time_1, fam_time_3, fam_time_2,
    fam_time_3, fam_time_2, fam_time_1
  )
  
  # Base row type sequence before reversals.
  if (stimulus_type_order == "fribble_first") {
    cur_row_type <- c(rep("fribble", 6), rep("fractal", 6))
  } else {
    cur_row_type <- c(rep("fractal", 6), rep("fribble", 6))
  }
  
  # Apply the same ordering logic to row type, time, and item sequences.
  ordered_row_type <- handle_reverse_ordering(cur_row_type, reverse_order_block, reverse_order_list)
  ordered_fam_time_list <- handle_reverse_ordering(fam_time_list, reverse_order_block, reverse_order_list)
  
  timeout_ordered_fam_time_list <- ordered_fam_time_list * 2
  
  # Balanced random location order: 6 left, 6 right.
  location_seed <- base_lab_id * 100000 + order_id * 10 + location_shuffle_group
  ordered_cur_test_familiar_location_list <- make_balanced_location_order(location_seed)
  
  switched_ordered_cur_test_familiar_location_list <- ifelse(
    ordered_cur_test_familiar_location_list == "left",
    "right",
    "left"
  )
  
  # Strict complexity assignment within each file.
  complexity_seed <- base_lab_id * 10000 + order_id
  ordered_cur_complexity_list <- make_strict_complexity(
    row_type_vec = ordered_row_type,
    time_vec = ordered_fam_time_list,
    seed = complexity_seed
  )
  
  if (complexity_polarity == "inverse") {
    ordered_cur_complexity_list <- invert_complexity(ordered_cur_complexity_list)
  }
  
  # Familiar / novel item identity.
  cur_familiar_fribble_items <- sapply(
    fribble_dict[[fribble_set]],
    function(pair) pair[familiar_role + 1]
  )
  cur_familiar_fractal_items <- sapply(
    fractal_dict[[fractal_set]],
    function(pair) pair[familiar_role + 1]
  )
  
  cur_novel_role <- ifelse(familiar_role == 0, 1, 0)
  
  cur_novel_fribble_items <- sapply(
    fribble_dict[[fribble_set]],
    function(pair) pair[cur_novel_role + 1]
  )
  cur_novel_fractal_items <- sapply(
    fractal_dict[[fractal_set]],
    function(pair) pair[cur_novel_role + 1]
  )
  
  # Build item order based on stimulus type order.
  if (stimulus_type_order == "fribble_first") {
    cur_familiar_items <- c(cur_familiar_fribble_items, cur_familiar_fractal_items)
    cur_novel_items <- c(cur_novel_fribble_items, cur_novel_fractal_items)
  } else {
    cur_familiar_items <- c(cur_familiar_fractal_items, cur_familiar_fribble_items)
    cur_novel_items <- c(cur_novel_fractal_items, cur_novel_fribble_items)
  }
  
  # Reverse item order to match the same structural ordering.
  ordered_cur_familiar_items <- handle_reverse_ordering(
    cur_familiar_items, reverse_order_block, reverse_order_list
  )
  ordered_cur_novel_items <- handle_reverse_ordering(
    cur_novel_items, reverse_order_block, reverse_order_list
  )
  
  # Build stimulus file names by row.
  build_image_name <- function(item, comp, row_type) {
    if (row_type == "fribble") {
      paste0(item, "_", capitalize_first(comp))
    } else {
      paste0("fractal_", comp, "_", item, "_bright")
    }
  }
  
  ordered_cur_familiar_images <- mapply(
    build_image_name,
    ordered_cur_familiar_items,
    ordered_cur_complexity_list,
    ordered_row_type,
    USE.NAMES = FALSE
  )
  
  ordered_cur_novel_images <- mapply(
    build_image_name,
    ordered_cur_novel_items,
    ordered_cur_complexity_list,
    ordered_row_type,
    USE.NAMES = FALSE
  )
  
  ordered_cur_familiar_images_path <- file.path(
    rel_image_path, paste0(ordered_cur_familiar_images, img_ext)
  )
  ordered_cur_novel_images_path <- file.path(
    rel_image_path, paste0(ordered_cur_novel_images, img_ext)
  )
  
  left_image_path_1 <- ifelse(
    ordered_cur_test_familiar_location_list == "left",
    ordered_cur_familiar_images_path,
    ordered_cur_novel_images_path
  )
  right_image_path_1 <- ifelse(
    ordered_cur_test_familiar_location_list == "right",
    ordered_cur_familiar_images_path,
    ordered_cur_novel_images_path
  )
  
  left_image_path_2 <- ifelse(
    switched_ordered_cur_test_familiar_location_list == "left",
    ordered_cur_familiar_images_path,
    ordered_cur_novel_images_path
  )
  right_image_path_2 <- ifelse(
    switched_ordered_cur_test_familiar_location_list == "right",
    ordered_cur_familiar_images_path,
    ordered_cur_novel_images_path
  )
  
  data.frame(
    lab_number = rep(lab_number, trial_num),
    base_lab_id = rep(base_lab_id, trial_num),
    order_id = rep(order_id, trial_num),
    trial_number = 1:trial_num,
    fribble_set = rep(fribble_set, trial_num),
    complexity_polarity = rep(complexity_polarity, trial_num),
    reverse_order_block = rep(reverse_order_block, trial_num),
    reverse_order_list = rep(reverse_order_list, trial_num),
    time_pair_group = rep(time_pair_group, trial_num),
    time_order_index = rep(time_order_index, trial_num),
    stimulus_type_order = rep(stimulus_type_order, trial_num),
    familiar_role = rep(familiar_role, trial_num),
    location_shuffle_group = rep(location_shuffle_group, trial_num),
    location_seed = rep(location_seed, trial_num),
    row_type = ordered_row_type,
    familiar_stimulus = ordered_cur_familiar_images,
    novel_stimulus = ordered_cur_novel_images,
    familiar_stimulus_item = ordered_cur_familiar_items,
    novel_stimulus_item = ordered_cur_novel_items,
    complexity_condition = ordered_cur_complexity_list,
    familiarization_time = ordered_fam_time_list,
    familiar_stimulus_path = ordered_cur_familiar_images_path,
    novel_stimulus_path = ordered_cur_novel_images_path,
    familiar_location_1 = ordered_cur_test_familiar_location_list,
    familiar_location_2 = switched_ordered_cur_test_familiar_location_list,
    left_image_path_1 = left_image_path_1,
    right_image_path_1 = right_image_path_1,
    left_image_path_2 = left_image_path_2,
    right_image_path_2 = right_image_path_2,
    test_time_1 = rep(test_time, trial_num),
    test_time_2 = rep(test_time, trial_num),
    familiarization_time_timeout = timeout_ordered_fam_time_list,
    stringsAsFactors = FALSE
  )
}

# ------------------------------------------------------------
# Generator
# ------------------------------------------------------------

generate_trials <- function() {
  output_dir <- file.path(getwd(), "trial_lists_768")
  dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
  
  # 24 base templates:
  # 2 fribble sets x 2 block reversals x 2 list reversals x 3 time-pair groups
  # Then duplicated with normal vs inverse complexity polarity.
  base_lab_templates <- expand.grid(
    fribble_set = c("set_1", "set_2"),
    reverse_order_block = c("base_block", "base_rev"),
    reverse_order_list = c("base", "rev"),
    time_pair_group = 1:3,
    stringsAsFactors = FALSE
  )
  
  lab_templates <- base_lab_templates[rep(seq_len(nrow(base_lab_templates)), each = 2), ]
  lab_templates$complexity_polarity <- rep(c("normal", "inverse"), times = nrow(base_lab_templates))
  lab_templates$base_lab_id <- rep(seq_len(nrow(base_lab_templates)), each = 2)
  
  if (nrow(lab_templates) != 48) {
    stop("Lab template count is not 48. Check the design.")
  }
  
  # 16 within-lab conditions:
  # 2 stimulus orders x 2 familiar roles x 2 location shuffle groups x 2 time orders
  lab_conditions <- expand.grid(
    stimulus_type_order = c("fribble_first", "fractal_first"),
    familiar_role = c(0, 1),
    location_shuffle_group = c(1, 2),
    time_order_index = c(1, 2),
    stringsAsFactors = FALSE
  )
  
  if (nrow(lab_conditions) != 16) {
    stop("Within-lab condition count is not 16. Check the design.")
  }
  
  generated_files <- character(0)
  global_order_id <- 1
  all_manifest_rows <- list()
  
  for (lab_idx in seq_len(nrow(lab_templates))) {
    lab_number <- lab_idx
    lab_spec <- lab_templates[lab_idx, ]
    
    lab_dir <- file.path(output_dir, sprintf("lab_%02d", lab_number))
    dir.create(lab_dir, recursive = TRUE, showWarnings = FALSE)
    
    lab_manifest <- data.frame(
      order_id = integer(0),
      lab_number = integer(0),
      base_lab_id = integer(0),
      fribble_set = character(0),
      complexity_polarity = character(0),
      reverse_order_block = character(0),
      reverse_order_list = character(0),
      time_pair_group = integer(0),
      stimulus_type_order = character(0),
      familiar_role = integer(0),
      location_shuffle_group = integer(0),
      time_order_index = integer(0),
      location_seed = integer(0),
      file_name = character(0),
      stringsAsFactors = FALSE
    )
    
    for (cond_idx in seq_len(nrow(lab_conditions))) {
      cond <- lab_conditions[cond_idx, ]
      
      location_seed <- lab_spec$base_lab_id * 100000 + global_order_id * 10 + cond$location_shuffle_group
      
      cur_df <- build_trial_df(
        order_id = global_order_id,
        lab_number = lab_number,
        base_lab_id = lab_spec$base_lab_id,
        complexity_polarity = lab_spec$complexity_polarity,
        fribble_set = lab_spec$fribble_set,
        reverse_order_block = lab_spec$reverse_order_block,
        reverse_order_list = lab_spec$reverse_order_list,
        time_pair_group = as.integer(lab_spec$time_pair_group),
        stimulus_type_order = cond$stimulus_type_order,
        familiar_role = as.integer(cond$familiar_role),
        location_shuffle_group = as.integer(cond$location_shuffle_group),
        time_order_index = as.integer(cond$time_order_index)
      )
      
      file_name <- sprintf("order_%03d.csv", global_order_id)
      output_path <- file.path(lab_dir, file_name)
      write.csv(cur_df, output_path, row.names = FALSE)
      
      generated_files <- c(generated_files, output_path)
      
      lab_manifest <- rbind(
        lab_manifest,
        data.frame(
          order_id = global_order_id,
          lab_number = lab_number,
          base_lab_id = lab_spec$base_lab_id,
          fribble_set = lab_spec$fribble_set,
          complexity_polarity = lab_spec$complexity_polarity,
          reverse_order_block = lab_spec$reverse_order_block,
          reverse_order_list = lab_spec$reverse_order_list,
          time_pair_group = as.integer(lab_spec$time_pair_group),
          stimulus_type_order = cond$stimulus_type_order,
          familiar_role = as.integer(cond$familiar_role),
          location_shuffle_group = as.integer(cond$location_shuffle_group),
          time_order_index = as.integer(cond$time_order_index),
          location_seed = location_seed,
          file_name = file_name,
          stringsAsFactors = FALSE
        )
      )
      
      global_order_id <- global_order_id + 1
    }
    
    write.csv(lab_manifest, file.path(lab_dir, "lab_manifest.csv"), row.names = FALSE)
    all_manifest_rows[[length(all_manifest_rows) + 1]] <- lab_manifest
  }
  
  write.csv(
    do.call(rbind, all_manifest_rows),
    file.path(output_dir, "all_order_assignment.csv"),
    row.names = FALSE
  )
  
  cat("Generated", length(generated_files), "CSV files in", output_dir, "\n")
  invisible(generated_files)
}

# ------------------------------------------------------------
# Checker helpers
# ------------------------------------------------------------

check_item_side_balance <- function(dfs, lab_folder, tolerance = 1) {
  records <- list()
  
  for (df in dfs) {
    fam_side <- ifelse(df$familiar_location_1 == "left", "left", "right")
    nov_side <- ifelse(df$familiar_location_1 == "left", "right", "left")
    
    records[[length(records) + 1]] <- data.frame(
      item = df$familiar_stimulus_item,
      side = fam_side,
      stringsAsFactors = FALSE
    )
    
    records[[length(records) + 1]] <- data.frame(
      item = df$novel_stimulus_item,
      side = nov_side,
      stringsAsFactors = FALSE
    )
  }
  
  item_side_data <- do.call(rbind, records)
  
  left_counts <- table(item_side_data$item[item_side_data$side == "left"])
  right_counts <- table(item_side_data$item[item_side_data$side == "right"])
  all_items <- sort(unique(item_side_data$item))
  
  side_report <- data.frame(
    lab_folder = basename(lab_folder),
    item = all_items,
    left_count = as.integer(left_counts[all_items]),
    right_count = as.integer(right_counts[all_items]),
    stringsAsFactors = FALSE
  )
  
  side_report$left_count[is.na(side_report$left_count)] <- 0
  side_report$right_count[is.na(side_report$right_count)] <- 0
  side_report$difference <- abs(side_report$left_count - side_report$right_count)
  side_report$balanced_ok <- side_report$difference <= tolerance
  
  lab_ok <- all(side_report$balanced_ok)
  
  list(
    item_side_report = side_report,
    lab_ok = lab_ok
  )
}

# ------------------------------------------------------------
# Checker for one lab
# ------------------------------------------------------------

check_lab_folder <- function(lab_dir) {
  files <- sort(list.files(lab_dir, pattern = "^order_[0-9]{3}\\.csv$", full.names = TRUE))
  
  if (length(files) == 0) {
    return(list(
      summary = data.frame(
        lab_folder = basename(lab_dir),
        n_files = 0,
        files_ok = FALSE,
        stimulus_balance_ok = FALSE,
        familiar_role_balance_ok = FALSE,
        location_shuffle_balance_ok = FALSE,
        time_balance_ok = FALSE,
        complexity_polarity_ok = FALSE,
        row_type_balance_ok = FALSE,
        strict_complexity_ok = FALSE,
        item_role_balance_ok = FALSE,
        item_side_balance_ok = FALSE,
        overall_ok = FALSE,
        notes = "No CSV files found",
        stringsAsFactors = FALSE
      ),
      files = data.frame(),
      items = data.frame(),
      side = data.frame()
    ))
  }
  
  dfs <- lapply(files, function(f) read.csv(f, stringsAsFactors = FALSE))
  
  file_summary <- do.call(
    rbind,
    lapply(seq_along(dfs), function(i) {
      df <- dfs[[i]]
      
      strict_ok <- TRUE
      for (stim in c("fribble", "fractal")) {
        for (t in c(5, 10, 15)) {
          idx <- which(df$row_type == stim & df$familiarization_time == t)
          if (length(idx) != 2) {
            strict_ok <- FALSE
          } else {
            ct <- table(df$complexity_condition[idx])
            if (!all(c("simple", "complex") %in% names(ct))) {
              strict_ok <- FALSE
            } else if (ct[["simple"]] != 1 || ct[["complex"]] != 1) {
              strict_ok <- FALSE
            }
          }
        }
      }
      
      data.frame(
        lab_folder = basename(lab_dir),
        file = basename(files[i]),
        order_id = unique(df$order_id)[1],
        stimulus_type_order = unique(df$stimulus_type_order)[1],
        familiar_role = unique(df$familiar_role)[1],
        location_shuffle_group = unique(df$location_shuffle_group)[1],
        time_order_index = unique(df$time_order_index)[1],
        complexity_polarity = unique(df$complexity_polarity)[1],
        row_fribble = count_or_zero(table(df$row_type), "fribble"),
        row_fractal = count_or_zero(table(df$row_type), "fractal"),
        loc_left = count_or_zero(table(df$familiar_location_1), "left"),
        loc_right = count_or_zero(table(df$familiar_location_1), "right"),
        time_5 = count_or_zero(table(df$familiarization_time), "5"),
        time_10 = count_or_zero(table(df$familiarization_time), "10"),
        time_15 = count_or_zero(table(df$familiarization_time), "15"),
        comp_simple = count_or_zero(table(df$complexity_condition), "simple"),
        comp_complex = count_or_zero(table(df$complexity_condition), "complex"),
        strict_complexity_ok = strict_ok,
        stringsAsFactors = FALSE
      )
    })
  )
  
  n_files <- nrow(file_summary)
  files_ok <- (n_files == 16)
  
  stim_tab <- table(file_summary$stimulus_type_order)
  stimulus_balance_ok <- all(c("fribble_first", "fractal_first") %in% names(stim_tab)) &&
    stim_tab[["fribble_first"]] == 8 &&
    stim_tab[["fractal_first"]] == 8
  
  role_tab <- table(file_summary$familiar_role)
  familiar_role_balance_ok <- all(c("0", "1") %in% names(role_tab)) &&
    role_tab[["0"]] == 8 &&
    role_tab[["1"]] == 8
  
  loc_shuffle_tab <- table(file_summary$location_shuffle_group)
  location_shuffle_balance_ok <- all(c("1", "2") %in% names(loc_shuffle_tab)) &&
    loc_shuffle_tab[["1"]] == 8 &&
    loc_shuffle_tab[["2"]] == 8
  
  time_order_tab <- table(file_summary$time_order_index)
  time_balance_ok <- all(c("1", "2") %in% names(time_order_tab)) &&
    time_order_tab[["1"]] == 8 &&
    time_order_tab[["2"]] == 8
  
  complexity_polarity_values <- unique(file_summary$complexity_polarity)
  complexity_polarity_ok <- length(complexity_polarity_values) == 1 &&
    complexity_polarity_values %in% c("normal", "inverse")
  
  row_type_balance_ok <- all(
    file_summary$row_fribble == 6,
    file_summary$row_fractal == 6
  )
  
  within_file_trial_balance_ok <- all(
    file_summary$loc_left == 6,
    file_summary$loc_right == 6,
    file_summary$time_5 == 4,
    file_summary$time_10 == 4,
    file_summary$time_15 == 4,
    file_summary$comp_simple == 6,
    file_summary$comp_complex == 6,
    file_summary$strict_complexity_ok
  )
  
  all_familiar_items <- unlist(lapply(dfs, function(df) df$familiar_stimulus_item))
  all_novel_items <- unlist(lapply(dfs, function(df) df$novel_stimulus_item))
  all_items <- sort(unique(c(all_familiar_items, all_novel_items)))
  
  familiar_counts <- table(all_familiar_items)
  novel_counts <- table(all_novel_items)
  
  item_detail <- data.frame(
    lab_folder = basename(lab_dir),
    item = all_items,
    familiar_count = as.integer(familiar_counts[all_items]),
    novel_count = as.integer(novel_counts[all_items]),
    stringsAsFactors = FALSE
  )
  
  item_detail$familiar_count[is.na(item_detail$familiar_count)] <- 0
  item_detail$novel_count[is.na(item_detail$novel_count)] <- 0
  item_detail$both_roles_present <- item_detail$familiar_count > 0 & item_detail$novel_count > 0
  
  item_role_balance_ok <- all(item_detail$both_roles_present)
  
  side_check <- check_item_side_balance(dfs, lab_dir, tolerance = 1)
  item_side_report <- side_check$item_side_report
  item_side_balance_ok <- side_check$lab_ok
  
  overall_ok <- files_ok &&
    stimulus_balance_ok &&
    familiar_role_balance_ok &&
    location_shuffle_balance_ok &&
    time_balance_ok &&
    complexity_polarity_ok &&
    row_type_balance_ok &&
    within_file_trial_balance_ok &&
    item_role_balance_ok &&
    item_side_balance_ok
  
  notes <- c()
  if (!files_ok) notes <- c(notes, paste0("Expected 16 files, found ", n_files))
  if (!stimulus_balance_ok) notes <- c(notes, "Stimulus order not balanced 8/8")
  if (!familiar_role_balance_ok) notes <- c(notes, "Familiar role not balanced 8/8")
  if (!location_shuffle_balance_ok) notes <- c(notes, "Location shuffle group not balanced 8/8")
  if (!time_balance_ok) notes <- c(notes, "Time-order index not balanced 8/8")
  if (!complexity_polarity_ok) notes <- c(notes, "Multiple complexity polarity values found within lab")
  if (!row_type_balance_ok) notes <- c(notes, "Row type not balanced 6 fribble / 6 fractal")
  if (!within_file_trial_balance_ok) notes <- c(notes, "One or more files failed internal structure checks")
  if (!item_role_balance_ok) {
    bad_items <- item_detail$item[!item_detail$both_roles_present]
    notes <- c(notes, paste0("Items missing one role: ", paste(bad_items, collapse = ", ")))
  }
  if (!item_side_balance_ok) notes <- c(notes, "One or more items are not approximately balanced left/right")
  
  if (length(notes) == 0) notes <- "OK" else notes <- paste(notes, collapse = "; ")
  
  summary <- data.frame(
    lab_folder = basename(lab_dir),
    n_files = n_files,
    files_ok = files_ok,
    stimulus_balance_ok = stimulus_balance_ok,
    familiar_role_balance_ok = familiar_role_balance_ok,
    location_shuffle_balance_ok = location_shuffle_balance_ok,
    time_balance_ok = time_balance_ok,
    complexity_polarity = if (length(complexity_polarity_values) == 1) complexity_polarity_values[1] else "mixed",
    complexity_polarity_ok = complexity_polarity_ok,
    row_type_balance_ok = row_type_balance_ok,
    within_file_trial_balance_ok = within_file_trial_balance_ok,
    item_role_balance_ok = item_role_balance_ok,
    item_side_balance_ok = item_side_balance_ok,
    overall_ok = overall_ok,
    notes = notes,
    stringsAsFactors = FALSE
  )
  
  list(
    summary = summary,
    files = file_summary,
    items = item_detail,
    side = item_side_report
  )
}

# ------------------------------------------------------------
# Checker for all labs
# ------------------------------------------------------------

check_all_labs <- function() {
  root_dir <- file.path(getwd(), "trial_lists_768")
  lab_report_file <- file.path(root_dir, "lab_balance_report.csv")
  file_report_file <- file.path(root_dir, "lab_file_detail_report.csv")
  item_report_file <- file.path(root_dir, "lab_item_detail_report.csv")
  side_report_file <- file.path(root_dir, "lab_item_side_report.csv")
  global_item_complexity_file <- file.path(root_dir, "global_item_complexity_report.csv")
  
  lab_dirs <- sort(list.files(root_dir, pattern = "^lab_[0-9]{2}$", full.names = TRUE))
  if (length(lab_dirs) == 0) {
    stop(paste0("No lab folders found in: ", root_dir))
  }
  
  summaries <- list()
  file_details <- list()
  item_details <- list()
  side_details <- list()
  global_complexity_records <- list()
  
  for (lab_dir in lab_dirs) {
    result <- check_lab_folder(lab_dir)
    summaries[[length(summaries) + 1]] <- result$summary
    file_details[[length(file_details) + 1]] <- result$files
    item_details[[length(item_details) + 1]] <- result$items
    side_details[[length(side_details) + 1]] <- result$side
    
    lab_files <- sort(list.files(lab_dir, pattern = "^order_[0-9]{3}\\.csv$", full.names = TRUE))
    lab_dfs <- lapply(lab_files, function(f) read.csv(f, stringsAsFactors = FALSE))
    
    for (df in lab_dfs) {
      global_complexity_records[[length(global_complexity_records) + 1]] <- data.frame(
        item = c(df$familiar_stimulus_item, df$novel_stimulus_item),
        complexity = c(df$complexity_condition, df$complexity_condition),
        stringsAsFactors = FALSE
      )
    }
  }
  
  lab_report <- do.call(rbind, summaries)
  file_report <- do.call(rbind, file_details)
  item_report <- do.call(rbind, item_details)
  side_report <- do.call(rbind, side_details)
  
  global_complexity_long <- do.call(rbind, global_complexity_records)
  comp_tab <- table(global_complexity_long$item, global_complexity_long$complexity)
  if (!"simple" %in% colnames(comp_tab)) comp_tab <- cbind(comp_tab, simple = 0)
  if (!"complex" %in% colnames(comp_tab)) comp_tab <- cbind(comp_tab, complex = 0)
  comp_tab <- comp_tab[, c("simple", "complex"), drop = FALSE]
  
  global_item_complexity_report <- data.frame(
    item = rownames(comp_tab),
    simple_count = as.integer(comp_tab[, "simple"]),
    complex_count = as.integer(comp_tab[, "complex"]),
    equal_ok = as.integer(comp_tab[, "simple"]) == as.integer(comp_tab[, "complex"]),
    stringsAsFactors = FALSE
  )
  
  write.csv(lab_report, lab_report_file, row.names = FALSE)
  write.csv(file_report, file_report_file, row.names = FALSE)
  write.csv(item_report, item_report_file, row.names = FALSE)
  write.csv(side_report, side_report_file, row.names = FALSE)
  write.csv(global_item_complexity_report, global_item_complexity_file, row.names = FALSE)
  
  print(lab_report)
  
  cat("\nOverall pass rate:", sum(lab_report$overall_ok), "of", nrow(lab_report), "labs passed\n")
  cat("Complexity polarity counts across labs:\n")
  print(table(lab_report$complexity_polarity))
  cat("\nGlobal item complexity balance:\n")
  print(global_item_complexity_report)
  cat("\nLab item-side balance report written to:", side_report_file, "\n")
  cat("Lab summary written to:", lab_report_file, "\n")
  cat("File-level report written to:", file_report_file, "\n")
  cat("Item-level report written to:", item_report_file, "\n")
  cat("Global item complexity report written to:", global_item_complexity_file, "\n")
  
  failed_items <- item_report[!item_report$both_roles_present, ]
  if (nrow(failed_items) > 0) {
    cat("\nItems missing one role in at least one lab:\n")
    print(failed_items)
  } else {
    cat("\nAll items appeared as both familiar and novel in every lab.\n")
  }
  
  imbalance_items <- global_item_complexity_report[!global_item_complexity_report$equal_ok, ]
  if (nrow(imbalance_items) > 0) {
    cat("\nItems not balanced simple/complex globally:\n")
    print(imbalance_items)
  } else {
    cat("\nAll items were balanced simple/complex globally.\n")
  }
  
  side_fail <- side_report[!side_report$balanced_ok, ]
  if (nrow(side_fail) > 0) {
    cat("\nItems not approximately balanced left/right within labs:\n")
    print(side_fail)
  } else {
    cat("\nAll items were approximately balanced left/right within labs.\n")
  }
  
  invisible(list(
    lab_report = lab_report,
    file_report = file_report,
    item_report = item_report,
    side_report = side_report,
    global_item_complexity_report = global_item_complexity_report
  ))
}

# ------------------------------------------------------------
# Run
# ------------------------------------------------------------

generate_trials()
check_all_labs()
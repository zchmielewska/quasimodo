import numpy as np
import pandas as pd
import os
import pandas.api.types
from quasimodo import utils
from datetime import datetime
from pathlib import Path
from tkinter import messagebox as msg


def create_job_list(settings):
    # Initiate data frame for the list of jobs
    job_list = pd.DataFrame(columns=["Number", "LeftFile", "RightFile", "TheSame", "Message"])

    # Blank tiles (as in scrabble)
    blank_tile_list = settings['blank_tile'].split(",")

    # If there is no <*> in paths, then don't use blank tiles
    if (not "<*>" in settings['lhs']) and (not "<*>" in settings['rhs']):
        blank_tile_list = ['']

    # If blank tile hasn't been set, the list contains one element with empty string
    incorrect_folder = False
    for blank_tile_element in blank_tile_list:
        lhs_replaced = settings['lhs'].replace("<*>", blank_tile_element)
        rhs_replaced = settings['rhs'].replace("<*>", blank_tile_element)
        lhs_type = "file" if (lhs_replaced[-4:] == ".csv" or lhs_replaced[-4:] == ".txt" or lhs_replaced[-4:] == ".tbl") else "folder" # todo: expand for different data types
        rhs_type = "file" if (rhs_replaced[-4:] == ".csv" or rhs_replaced[-4:] == ".txt" or rhs_replaced[-4:] == ".tbl") else "folder" # todo: expand for different data types
        lhs = Path(lhs_replaced)
        rhs = Path(rhs_replaced)

        # file + folder | folder + file
        if (lhs_type == "file" and rhs_type == "folder") or (lhs_type == "folder" and rhs_type == "file"):
            msg.showwarning("Inconsistent sources", "Left and right must be either both files or folders.")
        # file + file
        elif lhs_type == "file" and rhs_type == "file":
            job_list = job_list.append({"LeftFile": lhs, "RightFile": rhs}, ignore_index=True)
        # folder + folder
        elif lhs_type == "folder" and rhs_type == "folder":
            # Check if folders exist
            if not lhs.exists():
                msg.showwarning("Incorrect folder", "Left folder does not exist:\n" + str(lhs))
                incorrect_folder = True
                return job_list, incorrect_folder
            if not rhs.exists():
                msg.showwarning("Incorrect folder", "Right folder does not exist:\n" + str(rhs))
                incorrect_folder = True
                return job_list, incorrect_folder
            lhs_files = [f for f in os.listdir(lhs) if os.path.isfile(os.path.join(lhs, f))]
            rhs_files = [f for f in os.listdir(rhs) if os.path.isfile(os.path.join(rhs, f))]
            common_files = np.intersect1d(np.array(lhs_files), np.array(rhs_files))  # todo: add only csv files
            for common_file in common_files:
                lhs_file = os.path.join(lhs, common_file)
                rhs_file = os.path.join(rhs, common_file)
                job_list = job_list.append({"LeftFile": Path(lhs_file), "RightFile": Path(rhs_file)}, ignore_index=True)

    # Add numbers
    job_list['Number'] = job_list.reset_index().index+1
    return job_list, incorrect_folder


def run(settings, progress_bar, log):
    # Reset progressbar from previous job
    progress_bar['value'] = 0
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    utils.add_log(log, "\n" + "#" * 80)
    utils.add_log(log, "\nStarting job: " + timestamp + "\n")

    # Retrieve job_list / Leave program if folder(s) doesn't exist
    job_list, incorrect_folder = create_job_list(settings)
    if incorrect_folder:
        return

    # Prepare output file
    output_folder = utils.sanitize_output(settings)
    if not output_folder.exists():
        answer = msg.askyesno("Create output folder", "The output folder does not exist. Do you want to create it?")
        if answer is True:
            try:
                os.makedirs(output_folder)
                utils.add_log(log, "Created folder:\n" + str(output_folder))
            except OSError:
                msg.showwarning("Warning", "Creation of the directory %s failed" % str(output_folder))
                return
    output_filename = "quasimodo" + timestamp + ".xlsx"
    output_path = os.path.join(output_folder, output_filename)
    writer = pd.ExcelWriter(output_path)
    job_list.to_excel(writer, sheet_name="JobList", index=False)

    # Iterate over jobs
    no_jobs = len(job_list.index)
    for index, row in job_list.iterrows():
        # Log current tables
        utils.add_log(log, "[" + str(index+1) + "/" + str(no_jobs) + "]")
        utils.add_log(log, "Left:  " + str(row['LeftFile']))
        utils.add_log(log, "Right: " + str(row['RightFile']) + "\n")
        progress_bar['value'] = (index+1)/no_jobs * 100

        # Check if files exist
        if not row['LeftFile'].exists():
            # If it's the first file, don't continue
            if index == 0:
                msg.showwarning("Incorrect file", "Left file does not exist:\n" + str(row["LeftFile"]))
                return
            # If it's not the first file, skip the row
            job_list.loc[index, "Message"] = "Left file does not exist"
            continue

        if not row['RightFile'].exists():
            # If it's the first file, don't continue
            if index == 0:
                msg.showwarning("Incorrect file", "Right file does not exist:\n" + str(row["RightFile"]))
                return
            # If it's not the first file, skip the row
            job_list.loc[index, "Message"] = "Right file does not exist"
            continue

        # If there is a problem with reading a file, use an empty DataFrame to not break the program
        try:
            if settings['comment'] == "":
                lhs = pd.read_csv(row['LeftFile'], sep=settings['delimiter'], decimal=settings['decimal'])
            else:
                lhs = pd.read_csv(row['LeftFile'], sep=settings['delimiter'], decimal=settings['decimal'],
                                  comment=settings['comment'])
        except pd.errors.EmptyDataError:
            lhs = pd.DataFrame()
        try:
            if settings['comment'] == "":
                rhs = pd.read_csv(row['RightFile'], sep=settings['delimiter'], decimal=settings['decimal'])
            else:
                rhs = pd.read_csv(row['RightFile'], sep=settings['delimiter'], decimal=settings['decimal'],
                                  comment=settings['comment'])
        except pd.errors.EmptyDataError:
            rhs = pd.DataFrame()

        output, the_same_flag = compare(lhs, rhs, settings['columns_subset'], settings['numerical_precision'])
        output.to_excel(writer, sheet_name=str(row['Number']), index=False)
        job_list.loc[index, "TheSame"] = the_same_flag
        utils.add_log(log, "Files are the same.\n") if the_same_flag else utils.add_log(log, "Files are different.\n")

    job_list.to_excel(writer, sheet_name="JobList", index=False)
    writer.save()
    utils.add_log(log, "Created file:\n" + str(output_path))

    # Save settings for future use
    file = open("settings.txt", "w")
    file.write(str(settings))
    file.close()


def compare(lhs, rhs, columns_subset, numerical_precision):
    columns_subset_list = columns_subset.split(",")
    the_same_flag = True

    # There might be columns only in LHS or RHS
    #sorted(set(l1) & set(l2), key=l1.index)
    common_cols = np.intersect1d(np.array(lhs.columns), np.array(rhs.columns))
    lhs_only_cols = np.setdiff1d(np.array(lhs.columns), common_cols)
    rhs_only_cols = np.setdiff1d(np.array(rhs.columns), common_cols)

    # User can choose to compare only a subset of columns
    if columns_subset != "":
        common_cols = np.intersect1d(common_cols, np.array(columns_subset_list))
        lhs_only_cols = np.intersect1d(lhs_only_cols, np.array(columns_subset_list))
        rhs_only_cols = np.intersect1d(rhs_only_cols, np.array(columns_subset_list))

    # RHS has fewer rows
    if len(lhs) - len(rhs) > 0:
        no_rows_difference = len(lhs) - len(rhs)
        zero_like_row = []
        for c in rhs.columns:
            if pandas.api.types.is_numeric_dtype(rhs[c]):
                zero_like_row.append(0)
            else:
                zero_like_row.append("")
        zeros = pd.DataFrame(data=[zero_like_row], columns=list(rhs.columns))
        frames = [rhs, pd.concat([zeros] * no_rows_difference)]
        rhs = pd.concat(frames)

    # LHS has fewer rows
    if len(rhs) - len(lhs) > 0:
        no_rows_difference = len(rhs) - len(lhs)
        zero_like_row = []
        for c in lhs.columns:
            if pandas.api.types.is_numeric_dtype(lhs[c]):
                zero_like_row.append(0)
            else:
                zero_like_row.append("")
        zeros = pd.DataFrame(data=[zero_like_row], columns=list(lhs.columns))
        frames = [lhs, pd.concat([zeros] * no_rows_difference)]
        lhs = pd.concat(frames)

    output = pd.DataFrame(index=range(max(len(lhs), len(rhs))))

    # Compare common columns
    for col in common_cols:
        result = utils.compare_cols(lhs[col], rhs[col])
        output[col] = list(result)
        # the_same_flag is set to false when differences appear
        if pd.api.types.is_bool_dtype(output[col]):
            if not all(output[col]):
                the_same_flag = False
        elif pd.api.types.is_numeric_dtype(output[col]):
            if not all(abs(output[col]) < 10**numerical_precision):
                the_same_flag = False

    # Add LHS only cols
    for col in lhs_only_cols:
        output[col] = "only_in_left"

    # Add RHS only cols
    for col in rhs_only_cols:
        output[col] = "only_in_right"

    # Tables differ if they contain different columns
    if len(lhs_only_cols) > 0 or len(rhs_only_cols) > 0:
        the_same_flag = False

    return output, the_same_flag

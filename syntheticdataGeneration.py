def generate_data(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print(f"File uploaded that triggered Cloud Function for generating data  is : {file['name']}.")
    from google.cloud import storage
    from datetime import datetime,timedelta
    import json,random,secrets

    # Temporary file to write synthetic data into
    output_file = open("/tmp/SIT_manufactured_txn.csv","w")

    client = storage.Client()
    bucket = client.get_bucket('hari-bucket-2019')

    ### Read the customer accounts data from Cloud Storage bucket
    blob = bucket.get_blob('SyntheticData_Config/cust_profile_mapping.txt')
    #blob = bucket.get_blob(file['name'])
    str_blob = str(blob.download_as_string(),'utf-8')
    print (type(str_blob))
    cust_profile_mapping = json.loads(str_blob)
    #print (cust_profile_mapping["CUST_ACCT"]["911111111"])

    ### Read the Customer Account mapping data from Cloud Storage bucket
    blob2 = bucket.get_blob('SyntheticData_Config/cust_acct_profile.txt')
    str_blob2 = str(blob2.download_as_string(),'utf-8')
    #print (type(str_blob2))
    cust_acct_profile = json.loads(str_blob2)
    #print (cust_acct_profile["START_DATE"])

    ### Map the customer accounts with their transaction profiles
    for cust in cust_profile_mapping:
        for acct in cust_profile_mapping[cust]:
            for index,content in enumerate(cust_profile_mapping[cust][acct]):
                #print (index,content)
                cust_profile_mapping[cust][acct][index].update({"profile": cust_acct_profile[cust_profile_mapping[cust][acct][index]["profile"]]})
    print (cust_profile_mapping)

    txn_acct_bsb = 13310

    ### Write the header column
    print(
        "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
            "cust_no", "val_txn_id", "acct_id", "acct_num", "txn_acct_bsb", "prd_tp_cd", "plstc_logo",
            "acct_id_oth_party", "txn_efctv_dt", "txn_pstng_dt", "sys_tm", "crdt_dbt_cd", "txn_amt", "stmt_desc",
            "txn_desc", "on_stmt_ind_txt", "match_rvrsl_ind_txt", "intrnl_gen_txn_ind_txt", "mcc", "mcg_lvl_1_desc",
            "mcg_lvl_2_desc", "mcg_lvl_3_desc", "mrchnt_ctgry_desc", "txn_mrchnt_id", "rtler_id", "trmnl_id",
            "txn_trmnl_ownr_nm", "txn_trmnl_cty_nm", "txn_crd_issr_fi_cd", "n_user_de", "bpay_billr_cd", "bpay_ref_num",
            "bpay_payer_fi_cd", "trace_id", "ctm_txn_cd", "src_txn_cd", "ctm_chnl", "aux_dmcl", "extra_aux_dmcl",
            "txn_auth_cd", "posted_src_table", "ctm_src_sys_orgn", "txn_src_sys", "txn_channel", "txn_method",
            "txn_purpose", "tokenised_ind", "token_provider", "last_update_dt", "sys_tm_src", "acq_inst_id",
            "trmnl_cntry_cd", "src_txn_ccy_cd", "snapshot_date"))
    output_file.write(
        "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
            "cust_no", "val_txn_id", "acct_id", "acct_num", "txn_acct_bsb", "prd_tp_cd", "plstc_logo",
            "acct_id_oth_party", "txn_efctv_dt", "txn_pstng_dt", "sys_tm", "crdt_dbt_cd", "txn_amt", "stmt_desc",
            "txn_desc", "on_stmt_ind_txt", "match_rvrsl_ind_txt", "intrnl_gen_txn_ind_txt", "mcc", "mcg_lvl_1_desc",
            "mcg_lvl_2_desc", "mcg_lvl_3_desc", "mrchnt_ctgry_desc", "txn_mrchnt_id", "rtler_id", "trmnl_id",
            "txn_trmnl_ownr_nm", "txn_trmnl_cty_nm", "txn_crd_issr_fi_cd", "n_user_de", "bpay_billr_cd", "bpay_ref_num",
            "bpay_payer_fi_cd", "trace_id", "ctm_txn_cd", "src_txn_cd", "ctm_chnl", "aux_dmcl", "extra_aux_dmcl",
            "txn_auth_cd", "posted_src_table", "ctm_src_sys_orgn", "txn_src_sys", "txn_channel", "txn_method",
            "txn_purpose", "tokenised_ind", "token_provider", "last_update_dt", "sys_tm_src", "acq_inst_id",
            "trmnl_cntry_cd", "src_txn_ccy_cd", "snapshot_date"))

    ### Generate the synthetic data for every transaction for all customer accounts
    for cust in cust_profile_mapping["CUST_ACCT"]:
        for acct in cust_profile_mapping["CUST_ACCT"][cust]:
            for curr_profile in acct["profile"]:
                TXN_DATE = cust_acct_profile["START_DATE"]
                txn_count = 0
                while (datetime.strptime(TXN_DATE, "%Y-%m-%d") < datetime.strptime(cust_acct_profile["END_DATE"],"%Y-%m-%d")) and txn_count < curr_profile["max_txn_count"]:
                    if txn_count == 0:
                        TXN_DATE = curr_profile.get("start_date",cust_acct_profile["START_DATE"])  ### Use the Start Date if there is a custom date defined at the transaction level , Else use the Default START_DATE defined at the beginning
                    trace_id = secrets.token_hex(16)
                    # txn_efctv_dt = (datetime.strptime(TXN_DATE, "%Y-%m-%d") + timedelta(days=curr_profile["frequency_in_days"])).isoformat()
                    txn_efctv_dt = (datetime.strptime(TXN_DATE, "%Y-%m-%d")).isoformat()
                    txn_pstng_dt = txn_efctv_dt
                    last_update_dt = txn_efctv_dt
                    snapshot_date = txn_efctv_dt[0:txn_efctv_dt.index("T")]
                    # acct_balance += round(txn_amt * txn_sign, 2)
                    val_txn_id = random.randint(1185189290, 9185189290)
                    acct_id_oth_party = random.randint(2508482, 9250848)
                    acq_inst_id = random.randint(424500, 924500)
                    trmnl_cntry_cd = "AU"
                    src_txn_ccy_cd = random.choices(["AUD", "36", "356", ""], weights=[70, 20, 8, 2], k=1)[0]
                    on_stmt_ind_txt = "Yes"
                    match_rvrsl_ind_txt = random.choice(["No", "Not Applicable"])
                    intrnl_gen_txn_ind_txt = random.choice(["No", "Yes"])
                    # mcc = random.choice(["0", ""])
                    mcg_lvl_1_desc = mcg_lvl_2_desc = mcg_lvl_3_desc = mrchnt_ctgry_desc = txn_mrchnt_id = rtler_id = trmnl_id = txn_trmnl_ownr_nm = txn_trmnl_cty_nm = txn_crd_issr_fi_cd = n_user_de = bpay_ref_num = bpay_payer_fi_cd = txn_auth_cd = ctm_src_sys_orgn = acq_inst_id = trmnl_cntry_cd = ""
                    bpay_billr_cd = random.choice(["0", ""])
                    ctm_txn_cd = random.choice(["0", "50", "53", "89", "98"])
                    src_txn_cd = random.choice(["1048", "20001", "20002", "32801"])
                    ctm_chnl = random.choice(["514", "580", "622", "800", "801"])
                    aux_dmcl = random.choice(["0", "1950", "9047", "9063", "9066"])
                    extra_aux_dmcl = random.choice(["0", ""])
                    posted_src_table = random.choice(["LNS", "DMND_DPST"])
                    sys_tm_src = random.choice(["CTM", "POSTED - LNS"])
                    plstc_logo = ""
                    sys_tm = "1970-01-01 12:27:39.000"
                    tokenised_ind = "N"
                    token_provider = "Unclassified"
                    if curr_profile["subsequent_txn_amt_change_%"] == 0:  # If % change is 0
                        txn_amt = random.choice(curr_profile["txn_amt"])  # Just pick a random value from the list
                    else:  # Else generate continuosly increasing or decreasing amounts for subsequent transactions
                        txn_amt = curr_profile["txn_amt"][0] + txn_count * curr_profile["txn_amt"][0] * curr_profile[
                            "subsequent_txn_amt_change_%"] / 100
                    if curr_profile["crdt_dbt_cd"] == "Debit":
                        # debit_option = random.randint(0, len(DEBIT_INFO["options"]) - 1)
                        debit_option = curr_profile["txn_options_index"]
                        txn_purpose = cust_acct_profile["DEBIT_INFO"]["options"][debit_option]["txn_purpose"]
                        txn_desc = random.choice(cust_acct_profile["DEBIT_INFO"]["options"][debit_option]["txn_desc"])
                        txn_src_sys = random.choice(cust_acct_profile["DEBIT_INFO"]["options"][debit_option]["txn_src_sys"])
                        txn_channel = random.choice(cust_acct_profile["DEBIT_INFO"]["options"][debit_option]["txn_channel"])
                        txn_method = random.choice(cust_acct_profile["DEBIT_INFO"]["options"][debit_option]["txn_method"])
                    else:
                        # credit_option = random.randint(0, len(CREDIT_INFO["options"]) - 1)
                        credit_option = curr_profile["txn_options_index"]
                        txn_purpose = cust_acct_profile["CREDIT_INFO"]["options"][credit_option]["txn_purpose"]
                        txn_desc = random.choice(cust_acct_profile["CREDIT_INFO"]["options"][credit_option]["txn_desc"])
                        txn_src_sys = random.choice(cust_acct_profile["CREDIT_INFO"]["options"][credit_option]["txn_src_sys"])
                        txn_channel = random.choice(cust_acct_profile["CREDIT_INFO"]["options"][credit_option]["txn_channel"])
                        txn_method = random.choice(cust_acct_profile["CREDIT_INFO"]["options"][credit_option]["txn_method"])
                    # print(
                    #         "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                    #             cust, val_txn_id, acct["acct_id"], acct["acct_num"], txn_acct_bsb, curr_profile["prd_tp_cd"],
                    #             plstc_logo, acct_id_oth_party, txn_efctv_dt, txn_pstng_dt, sys_tm, curr_profile["crdt_dbt_cd"], random.choice(curr_profile["txn_amt"]),
                    #             random.choice(curr_profile["stmt_desc"]), txn_desc, on_stmt_ind_txt, match_rvrsl_ind_txt, intrnl_gen_txn_ind_txt, mcc,
                    #             mcg_lvl_1_desc, mcg_lvl_2_desc, mcg_lvl_3_desc, mrchnt_ctgry_desc, txn_mrchnt_id, rtler_id,
                    #             trmnl_id, txn_trmnl_ownr_nm, txn_trmnl_cty_nm, txn_crd_issr_fi_cd, n_user_de, bpay_billr_cd,
                    #             bpay_ref_num, bpay_payer_fi_cd, trace_id, ctm_txn_cd, src_txn_cd, ctm_chnl, aux_dmcl,
                    #             extra_aux_dmcl, txn_auth_cd, posted_src_table, ctm_src_sys_orgn, txn_src_sys, txn_channel,
                    #             txn_method, txn_purpose, tokenised_ind, token_provider, last_update_dt, sys_tm_src, acq_inst_id,
                    #             trmnl_cntry_cd, src_txn_ccy_cd, snapshot_date)
                    # )
                    output_file.write(
                        "{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                            cust, val_txn_id, acct["acct_id"], acct["acct_num"], txn_acct_bsb,
                            curr_profile["prd_tp_cd"],
                            plstc_logo, acct_id_oth_party, TXN_DATE, TXN_DATE, sys_tm, curr_profile["crdt_dbt_cd"],
                            txn_amt,
                            random.choice(curr_profile["stmt_desc"]), txn_desc, on_stmt_ind_txt, match_rvrsl_ind_txt,
                            intrnl_gen_txn_ind_txt, curr_profile["mcc"],
                            mcg_lvl_1_desc, mcg_lvl_2_desc, mcg_lvl_3_desc, mrchnt_ctgry_desc, txn_mrchnt_id, rtler_id,
                            trmnl_id, txn_trmnl_ownr_nm, txn_trmnl_cty_nm, txn_crd_issr_fi_cd, n_user_de, bpay_billr_cd,
                            bpay_ref_num, bpay_payer_fi_cd, trace_id, ctm_txn_cd, src_txn_cd, ctm_chnl, aux_dmcl,
                            extra_aux_dmcl, txn_auth_cd, posted_src_table, ctm_src_sys_orgn, txn_src_sys, txn_channel,
                            txn_method, txn_purpose, tokenised_ind, token_provider, last_update_dt, sys_tm_src,
                            acq_inst_id,
                            trmnl_cntry_cd, src_txn_ccy_cd, snapshot_date)
                    )
                    TXN_DATE = (datetime.strptime(TXN_DATE, "%Y-%m-%d") + timedelta(days=random.randint(curr_profile["frequency_in_days"][0],curr_profile["frequency_in_days"][1]))).strftime("%Y-%m-%d")
                    txn_count += 1
                    # print (cust,acct["acct_num"],TXN_DATE,curr_profile["crdt_dbt_cd"],random.choice(curr_profile["stmt_desc"]),random.choice(curr_profile["txn_amt"]))

    #output_file.write(str(cust_profile_mapping))
    output_file.close()

    ### Output bucket to write the generated synthetic data into
    ### This file can be downloaded and uploaded for further processing into a Consumption Table
    bucket2 = client.get_bucket('ingress_bucket')
    output_blob = bucket2.blob("SIT_manufactured_txn.csv")
    output_blob.upload_from_filename("/tmp/SIT_manufactured_txn.csv")

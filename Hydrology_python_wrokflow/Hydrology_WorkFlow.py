import os




print ("""




                      ###########################    ####################            
                      ###########################    ####################
                      ###########################    ####################      
                               ########                         #########   
                               ########                        #########
                               ########                       #########
                               ########                      #########
                               ########                     #########
                               ########                    #########
                               ########                   ######### 
                              ##########                 ###########


""")


def Hydrology_flow(first_step_input, second_Step_input, out_dir, exec_path):


    base_fir = os.path.dirname(os.path.abspath(__file__))

    if not os.path.exists(os.path.join(base_fir,out_dir)):
        os.makedirs(os.path.join(base_fir,out_dir))

    if not os.path.exists(os.path.join(base_fir,out_dir,"step1")):
        os.makedirs(os.path.join(base_fir,out_dir,"step1"))

    if not os.path.exists(os.path.join(base_fir,out_dir,'step2')):
        os.makedirs(os.path.join(base_fir,out_dir,"step2"))

    if not os.path.exists(os.path.join(base_fir,out_dir,"step3")):
        os.makedirs(os.path.join(base_fir,out_dir,"step3"))

    if not os.path.exists(os.path.join(base_fir,out_dir,"step4")):
        os.makedirs(os.path.join(base_fir,out_dir,"step4"))


    os.environ['exe_path'] = exec_path


    ###################### Step_1 ########################
    os.environ['first_step_input']  = first_step_input
    os.environ['out_first'] = os.path.join(base_fir,out_dir,'step1',"step1_out.csv")
    os.system('python $exe_path/bin/prepare_flood_events_table_NEW.py -I $first_step_input  -O $out_first ')
    ###################### Step_1 ########################



    ###################### Step_2 ########################
    os.environ['second_Step_input']  = second_Step_input
    os.environ['out_second'] = os.path.join(base_fir,out_dir,'step2',"step2_out.csv")
    os.system('python $exe_path/bin/make_dly_obs_table_standalone_NEW.py -I $second_Step_input -O $out_second' )
    ###################### Step_2 ########################


    ###################### Step_3 ########################
    os.environ['i1'] = os.path.join(base_fir,out_dir,'step1',"step1_out.csv")
    os.environ['i2'] = os.path.join(base_fir,out_dir,'step2',"step2_out.csv")
    os.environ['out_third'] = os.path.join(base_fir,out_dir,'step3',"step3_out.csv")
    os.system('python $exe_path/bin/by_event_for_model_NEW.py -i $i1 -I $i2 -O $out_third')
    ###################### Step_3 ########################


    ###################### Step_4 ########################
    os.environ['in_forth'] = os.path.join(base_fir,out_dir,'step3',"step3_out.csv")
    os.environ['out_forth'] = os.path.join(out_dir,"step4")
    os.system('Rscript $exe_path/bin/model_flood_counts_rf_ps_cln_NEW.r $in_forth $out_forth')
    ###################### Step_4 ########################



if __name__=="__main__":


    import argparse
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-f", "--flood_report_file",
                        required=True,
                        default=None,
                        help="flood report csv file")
                        
    parser.add_argument("-R", "--Rain_fall_Data",
                        required=True,
                        default=None,
                        help="Rain fall data")

    parser.add_argument("-O", "--Path_to_out_Dir",
                        required=False,
                        default=os.getcwd(),
                        help="out file directory")

    parser.add_argument("-e", "--exe_path",
                        required=False,
                        default=os.getcwd(),
                        help="scripts path")

                       
    args = parser.parse_args()
    Hydrology_flow(args.flood_report_file, args.Rain_fall_Data, args.Path_to_out_Dir, args.exe_path)








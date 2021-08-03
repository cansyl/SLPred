import os
import platform

def form_single_fasta_files(filename):
    if os.path.isdir("input_files") == False:
        os.mkdir("input_files")
    path_fasta = "input_files/fasta_files"
    path_single_fastas = "input_files/single_fastas"
    if os.path.isdir(path_single_fastas)==False:
        os.mkdir(path_single_fastas)
    count = 0

    with open("{}/{}.fasta".format(path_fasta, filename), "r") as fp:
        for line in fp:
            if line[0] == '>':
                count += 1
                fw_fasta = open("{}/{}_{}.fasta".format(path_single_fastas, filename, str(count)), "w")
            fw_fasta.write(line)
        fw_fasta.close()
    fp.close()
def form_pssm_files(filename2):
    path_single_fastas = "input_files/single_fastas"
    path_blast = "ncbi-blast"
    for filename in os.listdir(path_single_fastas):
        if filename.split("_")[0].strip() == filename2:
            inputfile = "{}/{}".format(path_single_fastas, filename)
            if os.path.isdir("input_files/pssm_files") == False:
                os.mkdir("input_files/pssm_files")
            pssmfile = "{}/{}/{}.pssm".format("input_files", "pssm_files", filename.split(".")[0].strip())
            if ("Linux" in str(platform.platform())):
                os.system("{}/psiblast -db {}/uniref50_db/uniref50.blastdb -evalue 0.001 -query {} "
                              "-out_ascii_pssm {}  -out outfile -num_iterations 3 -comp_based_stats 1"\
                      .format(path_blast, path_blast, inputfile, pssmfile))
            elif ("Darwin" in str(platform.platform())):
                print("{}/psiblastMAC -db {}/uniref50_db/uniref50.blastdb -evalue 0.001 -query {} "
                          "-out_ascii_pssm {}  -out outfile -num_iterations 3 -comp_based_stats 1" \
                          .format(path_blast, path_blast, inputfile, pssmfile))
                os.system("{}/psiblastMAC -db {}/uniref50_db/uniref50.blastdb -evalue 0.001 -query {} "
                          "-out_ascii_pssm {}  -out outfile -num_iterations 3 -comp_based_stats 1" \
                          .format(path_blast, path_blast, inputfile, pssmfile))

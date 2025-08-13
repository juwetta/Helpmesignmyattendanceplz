from multiprocessing import Process
import crawl
#import time

namelist = []

with open("namelist.txt", "r") as namelist_file:
    lines = namelist_file.readlines()
    namelist = [line.split(",") for line in lines]

# students = [["apkey1", "pass1"],
#             ["apkey2", "pass2"]]




def worker(num:int, otp:str = "000"):
    crawl.main(otp, apkey=namelist[num][0], password=namelist[num][1].strip("\n"))

def prompt_otp()->str:
    otp = ""
    while otp == "":
        otp = input("OTP>> ")

        if not otp.isdigit():
            print("invalid\n")
            otp = ""
    
    return otp

if __name__ == "__main__":
    otp = prompt_otp()
    processes = []
    process_num = len(namelist)

    for i in range(process_num):  
        p = Process(target=worker, args=(i,otp))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("All processes completed.")
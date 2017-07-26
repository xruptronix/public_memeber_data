from bs4 import BeautifulSoup

import requests
import csv

url = "http://www.rcpsych.ac.uk/asp/memlist/search.asp"

def get_grades():
    grades = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    options = soup.find("select",{"id":"grade"}).find_all("option")
    for option in options:
        if len(option.text.strip()) != 0:
            grades.append(option['value'])
    return grades

def main():
    url = "http://www.rcpsych.ac.uk/asp/memlist/results.asp"
    grades = get_grades()
    with open("memeber_list.csv","w+") as f:
        writer = csv.writer(f)
        writer.writerow(["First Name" ,"Last Name" , "Grade" , "Region"])

        for grade in grades:
            r = requests.post(url,data={"grade":grade})
            soup = BeautifulSoup(r.text,"html.parser")
            member_list = soup.find("table",{"class":"memlist"}).find_all("tr",{"class":"memlist"})
            for mem in member_list:
                tds = mem.find_all("td")
                full_name = tds[0].text.strip().encode("utf-8").split(" ")
                first_name = full_name[1]
                last_name = " ".join(full_name[2:])
                grade = tds[1].text.strip().encode("utf-8")
                region = tds[-1].text.strip().encode("utf-8")
                # print first_name,last_name,grade,region
                writer.writerow([first_name,last_name,grade,region])
            try:
                while True:
                    next_previous_tag = soup.find_all("a",{"class":"navBar"})[-1]
                    if "next" in next_previous_tag.text:
                        new_url = "http://www.rcpsych.ac.uk/asp/memlist/results.asp"+next_previous_tag['href'].strip()
                        r = requests.get(new_url)
                        soup = BeautifulSoup(r.text,"html.parser")
                        member_list = soup.find("table",{"class":"memlist"}).find_all("tr",{"class":"memlist"})
                        for mem in member_list:
                            tds = mem.find_all("td")
                            full_name = tds[0].text.strip().encode("utf-8").split(" ")
                            first_name = full_name[1]
                            last_name = " ".join(full_name[2:])
                            grade = tds[1].text.strip().encode("utf-8")
                            region = tds[-1].text.strip().encode("utf-8")
                            # print first_name,last_name,grade,region
                            writer.writerow([first_name,last_name,grade,region])
                    else:
                        break
            except:
                pass




if __name__ == "__main__":
    main()

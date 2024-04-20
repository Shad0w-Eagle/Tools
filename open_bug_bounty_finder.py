import argparse
import webbrowser
import requests
from tqdm import tqdm

ascii_art = """
 ██████╗ ██████╗ ███████╗███╗   ██╗    ██████╗ ██╗   ██╗ ██████╗                                    
██╔═══██╗██╔══██╗██╔════╝████╗  ██║    ██╔══██╗██║   ██║██╔════╝                                    
██║   ██║██████╔╝█████╗  ██╔██╗ ██║    ██████╔╝██║   ██║██║  ███╗                                   
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║    ██╔══██╗██║   ██║██║   ██║                                   
╚██████╔╝██║     ███████╗██║ ╚████║    ██████╔╝╚██████╔╝╚██████╔╝                                   
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝    ╚═════╝  ╚═════╝  ╚═════╝                                    
                                                                                                    
██████╗  ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗                                              
██╔══██╗██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝                                              
██████╔╝██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝                                               
██╔══██╗██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝                                                
██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║                                                 
╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝                                                 
                                                                                                    
██╗   ██╗██╗   ██╗██╗     ███╗   ██╗███████╗██████╗  █████╗ ██████╗ ██╗██╗     ██╗████████╗██╗   ██╗
██║   ██║██║   ██║██║     ████╗  ██║██╔════╝██╔══██╗██╔══██╗██╔══██╗██║██║     ██║╚══██╔══╝╚██╗ ██╔╝
██║   ██║██║   ██║██║     ██╔██╗ ██║█████╗  ██████╔╝███████║██████╔╝██║██║     ██║   ██║    ╚████╔╝ 
╚██╗ ██╔╝██║   ██║██║     ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║██╔══██╗██║██║     ██║   ██║     ╚██╔╝  
 ╚████╔╝ ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║██████╔╝██║███████╗██║   ██║      ██║   
  ╚═══╝   ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝╚══════╝╚═╝   ╚═╝      ╚═╝   
                                                                                                    
███████╗██╗███╗   ██╗██████╗ ███████╗██████╗     ██████╗ ██╗   ██╗                                  
██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗    ██╔══██╗╚██╗ ██╔╝                                  
█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝    ██████╔╝ ╚████╔╝                                   
██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗    ██╔══██╗  ╚██╔╝                                    
██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║    ██████╔╝   ██║                                     
╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═════╝    ╚═╝                                     
                                                                                                    
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗        ███████╗ █████╗  ██████╗ ██╗     ███████╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═████╗██║    ██║        ██╔════╝██╔══██╗██╔════╝ ██║     ██╔════╝
███████╗███████║███████║██║  ██║██║██╔██║██║ █╗ ██║        █████╗  ███████║██║  ███╗██║     █████╗  
╚════██║██╔══██║██╔══██║██║  ██║████╔╝██║██║███╗██║        ██╔══╝  ██╔══██║██║   ██║██║     ██╔══╝  
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝███████╗███████╗██║  ██║╚██████╔╝███████╗███████╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝"""

print(ascii_art)

def construct_url(domain):
    base_url = "https://www.openbugbounty.org/search/?search="
    return base_url + domain + "&researcher=&program="

def check_vulnerabilities(url):
    response = requests.get(url)
    if "0 vulnerability mirror(s) match your request" not in response.text:
        return True
    return False

def save_results(results, result_file):
    with open(result_file, "w") as file:
        for url in results:
            file.write(url + "\n")

def main():
    parser = argparse.ArgumentParser(description="Open Bug Bounty Finder CLI")
    parser.add_argument("-d", "--domain-file", dest="domain_file", help="Path to the file containing a list of domains")
    parser.add_argument("-o", "--output-file", dest="result_file", help="Path to the file to save the results")
    parser.add_argument("--open-browser", action="store_true", help="Automatically open URLs in browser without asking")
    args = parser.parse_args()

    if not args.domain_file or not args.result_file:
        parser.error("Please provide both domain file and result file.")

    if args.open_browser:
        open_in_browser = True
    else:
        open_in_browser_input = input("Do you want to open URLs in the browser? (yes/no): ")
        open_in_browser = open_in_browser_input.lower() == "yes"

    try:
        with open(args.domain_file, "r") as file:
            domains = file.readlines()
            processed_domains = []
            results = []
            for domain in tqdm(domains, desc="Checking domains", unit="domain"):
                domain = domain.strip()  # Remove any leading/trailing whitespace or newline characters
                url = construct_url(domain)
                if check_vulnerabilities(url):
                    print(f"Potential vulnerabilities found: {url}")
                    if open_in_browser:
                        webbrowser.open(url)
                    else:
                        results.append(url)
                processed_domains.append(domain)
                save_results(results, args.result_file)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Saving results...")
        save_results(results, args.result_file)
        print("Results saved successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Saving current progress...")
        save_results(results, args.result_file)
        print("Progress saved successfully.")

if __name__ == "__main__":
    main()

import argparse
import webbrowser
import requests
from tqdm import tqdm

ascii_art = """
 ██████╗ ██████╗ ███████╗███╗   ██╗    ██████╗ ██╗   ██╗ ██████╗     ██████╗  ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗   
██╔═══██╗██╔══██╗██╔════╝████╗  ██║    ██╔══██╗██║   ██║██╔════╝     ██╔══██╗██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝╚██╗ ██╔╝██╗
██║   ██║██████╔╝█████╗  ██╔██╗ ██║    ██████╔╝██║   ██║██║  ███╗    ██████╔╝██║   ██║██║   ██║██╔██╗ ██║   ██║    ╚████╔╝ ╚═╝
██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║    ██╔══██╗██║   ██║██║   ██║    ██╔══██╗██║   ██║██║   ██║██║╚██╗██║   ██║     ╚██╔╝  ██╗
╚██████╔╝██║     ███████╗██║ ╚████║    ██████╔╝╚██████╔╝╚██████╔╝    ██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║   ██║      ██║   ╚═╝
 ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝    ╚═════╝  ╚═════╝  ╚═════╝     ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝      ╚═╝      
                                                                                                                              
██████╗  █████╗ ████████╗ ██████╗██╗  ██╗███████╗██████╗        ██╗                                                           
██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗       ██║                                                           
██████╔╝███████║   ██║   ██║     ███████║█████╗  ██║  ██║    ████████╗                                                        
██╔═══╝ ██╔══██║   ██║   ██║     ██╔══██║██╔══╝  ██║  ██║    ██╔═██╔═╝                                                        
██║     ██║  ██║   ██║   ╚██████╗██║  ██║███████╗██████╔╝    ██████║                                                          
╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝     ╚═════╝                                                          
                                                                                                                              
██╗   ██╗███╗   ██╗██████╗  █████╗ ████████╗ ██████╗██╗  ██╗███████╗██████╗                                                   
██║   ██║████╗  ██║██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗                                                  
██║   ██║██╔██╗ ██║██████╔╝███████║   ██║   ██║     ███████║█████╗  ██║  ██║                                                  
██║   ██║██║╚██╗██║██╔═══╝ ██╔══██║   ██║   ██║     ██╔══██║██╔══╝  ██║  ██║                                                  
╚██████╔╝██║ ╚████║██║     ██║  ██║   ██║   ╚██████╗██║  ██║███████╗██████╔╝                                                  
 ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═════╝                                                   
                                                                                                                              
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
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝                          """

print(ascii_art)

def construct_url(domain):
    base_url = "https://www.openbugbounty.org/search/?search="
    return f"{base_url}{domain}&researcher=&program="

def check_vulnerabilities(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if "0 vulnerability mirror(s) match your request" not in response.text:
            return response.text.lower()
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")
    return ""

def save_results(unpatched_results, patched_results, result_file):
    if not unpatched_results and not patched_results:
        print("No results to save.")
        return

    try:
        with open(result_file, "w") as file:
            if unpatched_results:
                file.write("Unpatched URLs:\n")
                for url in unpatched_results:
                    file.write(url + "\n")
            if patched_results:
                file.write("\nPatched URLs:\n")
                for url in patched_results:
                    file.write(url + "\n")
        print(f"Results saved to {result_file}")
    except IOError as e:
        print(f"Error saving results: {e}")

def main():
    parser = argparse.ArgumentParser(description="Open Bug Bounty Finder CLI")
    parser.add_argument("-d", "--domain-file", help="Path to the file containing a list of domains")
    parser.add_argument("-D", "--domain", help="Single domain to check")
    parser.add_argument("-o", "--output-file", required=True, help="Path to the file to save the results")
    parser.add_argument("--open-browser", action="store_true", help="Automatically open URLs in the browser without asking")

    args = parser.parse_args()

    domains = []
    if args.domain_file:
        try:
            with open(args.domain_file, "r") as file:
                domains = [line.strip() for line in file if line.strip()]
        except IOError as e:
            print(f"Error reading domain file: {e}")
            return
    elif args.domain:
        domains.append(args.domain.strip())
    else:
        print("Please provide either a domain file with -d/--domain-file or a single domain with -D/--domain.")
        return

    open_in_browser = args.open_browser or input("Do you want to open URLs in the browser? (yes/no): ").strip().lower() == "yes"

    try:
        unpatched_results = []
        patched_results = []

        for domain in tqdm(domains, desc="Checking domains", unit="domain"):
            url = construct_url(domain)
            response_text = check_vulnerabilities(url)
            if response_text:
                if "unpatched" in response_text:
                    unpatched_results.append(url)
                    if open_in_browser:
                        webbrowser.open(url)
                elif "patched" in response_text:
                    patched_results.append(url)
                    if open_in_browser:
                        webbrowser.open(url)

        save_results(unpatched_results, patched_results, args.output_file)
    except KeyboardInterrupt:
        print("\nProgram interrupted. Saving results...")
        save_results(unpatched_results, patched_results, args.output_file)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Saving current progress...")
        save_results(unpatched_results, patched_results, args.output_file)

if __name__ == "__main__":
    main()


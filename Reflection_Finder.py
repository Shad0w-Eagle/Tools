import subprocess
import webbrowser
import asyncio
import aiofiles
from urllib.parse import urlparse, urlencode, parse_qs
from tqdm import tqdm

ascii_art = """
 ____       __ _           _   _                 _____ _           _             ____        
|  _ \ ___ / _| | ___  ___| |_(_) ___  _ __     |  ___(_)_ __   __| | ___ _ __  | __ ) _   _ 
| |_) / _ \ |_| |/ _ \/ __| __| |/ _ \| '_ \    | |_  | | '_ \ / _` |/ _ \ '__| |  _ \| | | |
|  _ <  __/  _| |  __/ (__| |_| | (_) | | | |   |  _| | | | | | (_| |  __/ |    | |_) | |_| |
|_| \_\___|_| |_|\___|\___|\__|_|\___/|_| |_|___|_|   |_|_| |_|\__,_|\___|_|    |____/ \__, |
 ____  _               _  ___             _|_____|         _                           |___/ 
/ ___|| |__   __ _  __| |/ _ \__      __ | ____|__ _  __ _| | ___                            
\___ \| '_ \ / _` |/ _` | | | \ \ /\ / / |  _| / _` |/ _` | |/ _ \                           
 ___) | | | | (_| | (_| | |_| |\ V  V /  | |__| (_| | (_| | |  __/                           
|____/|_| |_|\__,_|\__,_|\___/  \_/\_/___|_____\__,_|\__, |_|\___|                           
                                    |_____|          |___/                                   
"""

print(ascii_art)

async def send_curl_request(url, reflection_term, sem, progress):
    async with sem:
        try:
            process = await asyncio.create_subprocess_exec(
                "curl", "-s", "-L", url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            decoded_stdout = stdout.decode()
            if reflection_term in decoded_stdout:
                return url
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"An error occurred for URL: {url}, Error: {e}")
    return None

async def update_progress(progress):
    while True:
        progress.refresh()
        await asyncio.sleep(0.1)

async def check_endpoints(endpoints_file, reflection_term):
    sem = asyncio.Semaphore(1000)  # Increase semaphore limit
    reflection_urls = []

    async with aiofiles.open(endpoints_file, 'r') as file:
        lines = await file.readlines()
        progress = tqdm(total=len(lines), desc="Checking Endpoints", unit="Endpoint")
        for line in lines:
            endpoint = line.strip()
            modified_url = append_reflection_to_params(endpoint, reflection_term)
            url = await send_curl_request(modified_url, reflection_term, sem, progress)
            if url:
                reflection_urls.append(url)
            progress.update(1)
        progress.close()

    return reflection_urls

def append_reflection_to_params(url, reflection_term):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    for key in query_params:
        query_params[key] = [param + reflection_term for param in query_params[key]]
    modified_query = urlencode(query_params, doseq=True)
    modified_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{modified_query}"
    return modified_url

async def save_reflection_urls(reflection_urls, output_file):
    async with aiofiles.open(output_file, 'w') as file:
        for url in reflection_urls:
            await file.write(url + '\n')

async def main():
    endpoints_file = input("Enter the file path containing the list of endpoints: ")
    reflection_term = input("Enter the reflection term to append to each parameter: ")
    output_file = "Reflection_urls.txt"

    reflection_urls = await check_endpoints(endpoints_file, reflection_term)
    if reflection_urls:
        print("\nURLs with reflection term found in their responses:")
        for url in reflection_urls:
            webbrowser.open(url)
            print(url)
        await save_reflection_urls(reflection_urls, output_file)
        print(f"\nReflection URLs saved to '{output_file}'.")
    else:
        print("\nNo URLs with reflection term found in their responses.")

if __name__ == "__main__":
    asyncio.run(main())

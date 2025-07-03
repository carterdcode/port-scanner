## ⚠️ Disclaimer

This tool is intended **for educational and authorized security testing purposes only**.

- **Do not** use this tool against networks, systems, or devices you do not own or have explicit permission to test.
- Unauthorized scanning may be illegal and could result in criminal charges.

By using this tool, you agree that the author(s) are **not responsible** for any misuse or damages caused.

Use responsibly.

To use the tool from the commandline simply navigate to the src directory and run the command python port-scanner.py HostAddress -p Port-Range -n NumberOfThreads 
For example:
python port-scanner.py 192.168.0.1 -p 1-5000 -n 100 
You can also leave the port range and number of threads blank and it will use the default values.


You can also run this program using docker. 
Navigate to portscanner/src 
Then enter the following commands in the command line
docker build -t port-scanner .
docker run --rm -it port-scanner 192.168.1.238 -p 1-10 -n 1



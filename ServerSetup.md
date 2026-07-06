# Allow Connections to the WSL Backend

By default, services running inside WSL are only accessible from the local machine. To allow other devices on your network to connect to the FastAPI backend, create a Windows port proxy and allow the port through the Windows Firewall.

## 1. Open PowerShell as Administrator

Search for **PowerShell**, right-click it, and select **Run as administrator**.

## 2. Create a Port Proxy

Replace `YOUR_WSL_IP` with your current WSL IP address.

```powershell
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=3000 connectaddress=YOUR_WSL_IP connectport=3000
```

Example:

```powershell
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=3000 connectaddress=172.29.201.45 connectport=3000
```

## 3. Allow the Port Through Windows Firewall

Run the following command:

```powershell
New-NetFirewallRule -DisplayName "FastAPI 3000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 3000
```

## Notes

- If your WSL IP address changes after restarting WSL or rebooting Windows, update the port proxy with the new IP.
- This only needs to be configured on the Windows host. No additional firewall configuration is required inside WSL for a default Ubuntu installation.
- Once configured, devices on your local network can connect to the FastAPI backend using your Windows machine's IP address on port **3000**.

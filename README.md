# Qcells Cloud Home Assistant Integration

A Home Assistant custom integration for Qcells Cloud solar inverters.

 

## Features

- Real-time data retrieval from Qcells Cloud API
- Automatic sensor creation for power, energy, battery status, and more
- Configurable polling interval
- Secure credential management

## Installation

### Method 1: Manual Installation

1. Copy the `custom_components/qcells_cloud/` directory to your Home Assistant `config/custom_components/` directory.

2. Restart Home Assistant.

3. Go to **Settings > Devices & Services > Add Integration**.

4. Search for "Qcells Cloud" and follow the setup wizard.

#### Example SSH / host shell commands

If you are connected to the Home Assistant VM via SSH or are using the Home Assistant OS CLI, you need a real shell first.

In the HA OS CLI (`ha>` prompt), run:

```bash
login
```

After that you should see a shell prompt like `#`.

Then use the normal shell commands:

```bash
cd /config/custom_components
```

If `/config/custom_components` does not exist, try:

```bash
cd /mnt/data/supervisor/homeassistant/custom_components
```

Then clone or update the repo:

```bash
# clone the repository once into the qcells_cloud folder
git clone https://github.com/<your-username>/qcells_cloud_integration_scaffold.git qcells_cloud

# if the repo already exists, update it from main
git -C qcells_cloud pull origin main
```

Note: In Home Assistant OS, the built-in shell often does not include `git` and you cannot install it there with `sudo` or `apt`.
If `git` is not available, use one of these alternatives:

- Use the SSH add-on or Web Terminal add-on that provides a shell with `git`.
- Copy the `custom_components/qcells_cloud` folder from another machine via Samba, SCP, or USB.
- Download the repository on your PC and upload it into `config/custom_components/qcells_cloud`.

### Method 2: HACS (Recommended)

This integration is available through HACS (Home Assistant Community Store).

1. Add this repository to HACS as a custom repository.
2. Install the "Qcells Cloud" integration.
3. Restart Home Assistant and configure through the UI.

## Configuration

During setup, you will need to provide:

- **Base URL**: The Qcells Cloud API endpoint (usually pre-filled)
- **LAN Adapter Registration Number**: Your Qcells LAN adapter registration number (NOT the inverter device SN)
- **API Key**: Your Qcells Cloud API token
- **Polling Interval**: How often to fetch data (10-600 seconds)

> Note: `feedinpowerM2` represents an additional inverter output that is not controllable. The integration also exposes a computed sensor `Total PV Power` that adds `powerdc1` + `powerdc2` + `powerdc3` + `powerdc4` + `feedinpowerM2`.

`feedinpowerM2` is reported separately as `Extra inverter power`; this value represents an additional non-controllable inverter output.

If `powerdc3` or `powerdc4` are null or zero, the calculation still works and treats them as zero.

## Available Sensors

The integration creates the following sensors:

### Power & Energy
- AC Power (W)
- Feed-in Power (W)
- Total PV Power (W) — calculated from `powerdc1` + `powerdc2` + `powerdc3` + `powerdc4` + `feedinpowerM2`
- Extra inverter power (W) — `feedinpowerM2`, an additional non-controllable inverter output
- Battery Power (W)
- Daily Energy Yield (kWh)
- Total Energy Yield (kWh)

### Battery
- State of Charge (%)
- Battery Status

### DC Strings
- DC Power per string (W)

### System
- Inverter Status
- Last Update Time

## API Testing

To test the Qcells API independently:

1. **Set up environment variables:**
   ```bash
   # For development: Copy the example configuration file
   cp .env.example .env
   # Edit .env with your actual values

   # For production: The .env_prod file is loaded automatically if present
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the test script:**
   ```bash
   cd custom_components/qcells_cloud
   python test_api.py
   ```

## Security

- API credentials are stored securely in Home Assistant's configuration
- Environment files (`.env`, `.env_prod`) are excluded from version control
- Never commit sensitive credentials to the repository

## Troubleshooting

### Common Issues

1. **"Invalid token" error**: Check your API key and LAN adapter registration number
2. **Connection timeout**: Verify your internet connection and Qcells Cloud availability
3. **Missing sensors**: Restart Home Assistant after configuration

### Debug Mode

Enable debug logging in Home Assistant:

```yaml
logger:
  logs:
    custom_components.qcells_cloud: debug
```

### HACS unknown error

If HACS shows an "unknown error," try the manual installation method above first. This usually means the repository metadata or HACS repository scan did not complete correctly, but the integration can still work when installed manually.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This integration is not officially affiliated with Qcells or Hanwha. Use at your own risk.


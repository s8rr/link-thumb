# Discord Bot with Thumbnail Processing

This bot processes YouTube video links from Discord channels and provides functionalities like thumbnail generation and link processing. Users can toggle options like thumbnail size, embed color, description visibility, and more. Additionally, the bot can process existing links in a specific source channel and send thumbnails to a destination channel.

---

## Features

1. **Dynamic Embed Options:**
   - Toggle thumbnail size (large/small).
   - Enable or disable video descriptions.
   - Toggle video titles.
   - Change embed colors.
   - Reset settings.
   - Disable embed and show only the thumbnail.

2. **Thumbnail Processing:**
   - Extract and display video thumbnails for YouTube links.
   - Process existing links from a source channel.
   - Send thumbnails to a destination channel.

3. **Channel Configuration:**
   - Set a source channel to read existing links.
   - Set a destination channel to send processed thumbnails.

4. **Commands:**
   - `!setsource <channel_id>`: Set the source channel for link processing.
   - `!setdestination <channel_id>`: Set the destination channel for thumbnails.
   - `!processlinks`: Fetch and process existing links from the source channel.
   - Dynamic menu for toggling embed options.

---

## Prerequisites

- Python 3.10 or later.
- Required libraries:
  - `discord.py` (for interacting with Discord API).
  - `yt-dlp` (for processing YouTube video information).

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/s8rr/link-thumb.git
   cd link-thumb
   ```

2. **Install Dependencies:**
   ```bash
   pip install discord.py yt-dlp
   ```

3. **Set Up Bot Token:**
   - Create a bot on the [Discord Developer Portal](https://discord.com/developers/applications).
   - Copy the bot token and paste it into the `TOKEN` variable in the script.

---

## Usage

1. **Run the Bot:**
   ```bash
   python bot.py
   ```

2. **Interact with the Bot:**
   - Use the commands listed in the Features section.
   - The bot automatically processes links and manages embeds based on user toggles.

---

## Commands

| Command                  | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `!setsource <channel_id>` | Set the source channel for link processing.                               |
| `!setdestination <channel_id>` | Set the destination channel for thumbnails.                           |
| `!processlinks`          | Fetch and process existing links from the source channel.                 |

---

## Customization

- Modify the default settings in the `default_settings` dictionary.
- Extend the bot with additional commands as needed.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Troubleshooting

- **Signature Extraction Errors:** Ensure `yt-dlp` is up-to-date:
  ```bash
  pip install --upgrade yt-dlp
  ```
- **Bot Not Responding:** Verify the bot has the correct permissions for the channel.

---

## Contributions

Contributions are welcome! Feel free to submit a pull request or open an issue for any bugs or feature requests.


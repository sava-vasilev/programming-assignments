const Discord = require("discord.js");
// require("dotenv").config();

const TOKEN = "OTMyMjI2NTU3MjkwODg5MjE2.YeP5ow.vvvZWC3j1JXXUf7-3jF96vmQYzo";

const client = new Discord.Client({
  intents: ["GUILDS", "GUILD_MESSAGES"],
});

client.on("ready", () => {
  console.log(`Logged in as ${client.user.tag}`);
});

client.on("messageCreate", (message) => {
  if (message.content == "hello") {
    message.reply("world!");
  }
});

client.login(TOKEN);

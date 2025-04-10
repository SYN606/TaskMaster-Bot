import discord
from discord.ext import commands
import aiohttp
import os
from utils.config import EMOJIS, WEATHER_API_KEY


class Weather(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_key = WEATHER_API_KEY

        if not self.api_key:
            print(
                f"{EMOJIS['fail']} WEATHERAPI_KEY is not set in environment variables!"
            )

    @commands.hybrid_command(name="weather",
                             description="Get weather information for a city.")
    async def fetch_weather(self,
                            ctx: commands.Context,
                            *,
                            city: str = None):  # type: ignore
        if not self.api_key:
            return await ctx.send(
                f"{EMOJIS['fail']} Weather API key is missing. Contact the bot owner."
            )

        if not city:
            return await ctx.send(
                f"{EMOJIS['red_dot']} Please specify a city. Example: `/weather London`"
            )

        url = "http://api.weatherapi.com/v1/forecast.json"
        params = {"key": self.api_key, "q": city, "days": 1, "aqi": "yes"}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    embed = discord.Embed(
                        title=f"{EMOJIS['fail']} Error",
                        description=
                        "City not found! Please enter a valid city name.",
                        color=discord.Color.red())
                    return await ctx.send(embed=embed)

                data = await response.json()
                location = data["location"]["name"]
                country = data["location"]["country"]
                current = data["current"]
                forecast = data["forecast"]["forecastday"][0]

                embed = discord.Embed(
                    title=
                    f"{EMOJIS['mc_emerald']} Weather in {location}, {country}",
                    description=f"**{current['condition']['text']}**",
                    color=discord.Color.blue())
                embed.set_thumbnail(
                    url=f"https:{current['condition']['icon']}")
                embed.set_author(name=ctx.author.display_name,
                                 icon_url=ctx.author.display_avatar.url)

                embed.add_field(
                    name="🌡 Temperature",
                    value=f"{current['temp_c']}°C / {current['temp_f']}°F",
                    inline=True)
                embed.add_field(
                    name=f"{EMOJIS['mc_heart']} Feels Like",
                    value=
                    f"{current['feelslike_c']}°C / {current['feelslike_f']}°F",
                    inline=True)
                embed.add_field(
                    name=f"{EMOJIS['ping']} Wind",
                    value=
                    f"{current['wind_kph']} kph / {current['wind_mph']} mph",
                    inline=True)

                embed.add_field(
                    name="🌤 Forecast",
                    value=
                    f"High: {forecast['day']['maxtemp_c']}°C / {forecast['day']['maxtemp_f']}°F\n"
                    f"Low: {forecast['day']['mintemp_c']}°C / {forecast['day']['mintemp_f']}°F",
                    inline=True)

                embed.add_field(name="💧 Humidity",
                                value=f"{current['humidity']}%",
                                inline=True)
                embed.add_field(name="☁️ Cloud Cover",
                                value=f"{current['cloud']}%",
                                inline=True)
                embed.add_field(name="🌅 Sunrise",
                                value=forecast['astro']['sunrise'],
                                inline=True)
                embed.add_field(name="🌇 Sunset",
                                value=forecast['astro']['sunset'],
                                inline=True)
                embed.add_field(
                    name="🌙 Moon Phase",
                    value=
                    f"{forecast['astro']['moon_phase']} ({forecast['astro']['moon_illumination']}% illumination)",
                    inline=True)
                embed.add_field(
                    name="🔭 Visibility",
                    value=
                    f"{current['vis_km']} km / {current['vis_miles']} miles",
                    inline=True)
                embed.add_field(name="☀️ UV Index",
                                value=f"{current['uv']}",
                                inline=True)
                embed.add_field(
                    name="📏 Pressure",
                    value=
                    f"{current['pressure_mb']} mb / {current['pressure_in']} in",
                    inline=True)
                embed.add_field(
                    name=f"{EMOJIS['ban']} Precipitation",
                    value=f"{forecast['day']['totalprecip_mm']} mm",
                    inline=True)

                embed.set_footer(text="Powered by WeatherAPI.com")

                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Weather(bot))

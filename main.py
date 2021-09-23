import argparse
import time

from bot.icelakes_bot import IceLakesBot

parser = argparse.ArgumentParser()
parser.add_argument(
    "-t",
    "--time",
    default=10.,
    help="A float number of minutes how long should bot work(default: 10.0)"
)
parser.add_argument(
    "-p",
    "--pixels",
    default=50,
    help="A integer number of pixels how wide should rod go from left to right from center of the screen"
)
parser.add_argument(
    "--save-img", 
    action="store_true",
    help="Argument holding True value if called program will save imgs of frames when he got fish and evry 150 s img of straight rod"
)
args = parser.parse_args()

SAVE_IMG = bool(args.save_img)

TIME = float(args.time) * 60

PIXELS = int(args.pixels)

def main():
    print("Preparing bot...")
    bot = IceLakesBot(TIME, PIXELS, SAVE_IMG)

    print("Starting... ", end="")
    time.sleep(1.)

    for i in range(3, 0, -1):
        print(i, end=" ")
        time.sleep(1.)

    print("\nSTART")

    bot.run()

    print("FINISH")

if __name__ == "__main__":
    main()

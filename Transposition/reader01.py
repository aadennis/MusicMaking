def get_song_lines(file):
    with open(file, 'r') as f:
            return f.readlines()
         
def main(file):
    lines = get_song_lines(file)
    for line in lines:
            print(line)

if __name__ == "__main__":
  song_file = 'test_data/AHardDaysNight.txt'
  main(song_file)
seeds = []

# def make_row(chars):
#     row = []
#     for c in chars:

recording = False

with open("lexicon/lexicon.txt", 'r') as f:
    index = 0
    
    current_seed = []
    for line in f:
        chars = list(line)
        
        right_type = [(c == "*" or c == "." or c == "\t" or c == "\n") for c in chars]
        if all(right_type) and len(chars) > 1:
            if not recording:
                recording = True
                
            current_seed.append(line[1:-1])
            
        if not all(right_type):
            
            if recording:
                
                seeds.append(current_seed)
                current_seed = []

            recording = False

print(len(seeds))

for seed in seeds:
    for line in seed:
        print(line)

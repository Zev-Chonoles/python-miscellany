#  This brief function takes in a list of objects of any type, and 
#  outputs the object (or objects) that occurred most often, which
#  is usually called the "mode".
#
#  I just made this for fun and practice, without looking at anyone's
#  approach for how to do this.
#  Relevant SO thread is http://stackoverflow.com/q/10797819/

def most_freq(my_list):
    freq_dict = {}
    for x in my_list:
	if x in freq_dict:
     	    freq_dict[x] += 1
	else:
	    freq_dict[x] = 1
    highest_freq = 0
    keys_with_highest_freq = []
    for x in freq_dict:
	if freq_dict[x] == highest_freq:
    	    keys_with_highest_freq.append(x)
	if freq_dict[x] > highest_freq:
	    highest_freq = freq_dict[x]
	    keys_with_highest_freq = [x]
    return keys_with_highest_freq

some_numbers = [1,3,2,2,2,3,4,2,1,5,5,2,5,1,1,5,5]
print("Most frequent were: %s" % str(sorted(most_freq(some_numbers))).strip('[]'))
# Prints "Most frequent were: 2, 5"

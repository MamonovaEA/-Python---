def count_letter(word_list, letter):
  result = 0
  for word in word_list:
    if letter in word:
      result += 1
  return result

print(count_letter(['python', 'c++', 'c', 'scala', 'java'], 'c'))
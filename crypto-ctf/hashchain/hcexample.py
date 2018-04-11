import md5 #Must be run in python 2.7.x

#code used to calculate successive hashes in a hashchain.
id = "2183"
seed = md5.new(id).hexdigest()

#this will find the 5th hash in the hashchain. This would be the correct response if prompted with the 6th hash in the hashchain
count = 0
hashc = seed
count = 0
while True:
  prev = hashc
  hashc = md5.new(hashc).hexdigest()
  count += 1
  if hashc == "cb963b46825bc6170f3d5202b9bb3b0f":
  	print "FOUND", prev
  	break
  print hashc, count


print hashc, count

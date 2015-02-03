1) Corpus (new_corpus.txt)
2) Run cleancorpus.py. Gives new_step1.dat
3) Run $ tr " " "\n" < new_step1.dat > new_step2.dat
    This will give all words on different lines.
4) Run new_uniq.py. Gives new_step33.dat
5) This file contains the top 30,000 words and their frequency in the corpus.
6) Now, we use new_step33.dat and new_step1.dat to generate input corpus. Run list_to_input.py. Gives input_dataset#.dat
7) We shuffle the lines in input_dataset#.dat to give a random input to the NN. (There are too many lines to run every line). We then take this input to the NN.
   $ shuf -o input_dataseteN.dat input_dataset#.dat
8) We run try_answer.py. This trains the neural network on a shuffled input, and saves the progress every 10000 lines. Additionally, it can be run with the .pkl file as an input parameter to continue training on a re-shuffled input at any time. This NN has been coded especially for this type of net:

Input                              Hidden                   Output

word_vector[1..30000] -W1-> new_feature_vector[1..40] \
                                                       \
word_vector[1..30000] -W1-> new_feature_vector[1..40] \ \
                                                       \ \
word_vector[1..30000] -W1-> new_feature_vector[1..40] --W2--> output[1]
                                                       / /
word_vector[1..30000] -W1-> new_feature_vector[1..40] / /
                                                       /
word_vector[1..30000] -W1-> new_feature_vector[1..40] /


where all the weights in W1 are always the same.

9) We then run map_words.py to get the 40-dimensional feature vectors for every word in our 30000-length vocabulary. Gives prog.dat

10) We can use multiple methods of postprocessing to deal with this. postprocessing.py deals with NN calculation, and (to some extent) hierarchical clustering. Gives nn9m.dat

--

TODO:

Add Autoencoder algorithm
Add test tasks (Possibly odd-one-out approach, similar to Pranjal)
Compare with word2vec and glove

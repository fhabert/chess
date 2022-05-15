1) Les pieces ont été **découpé et sauvegarder en png** au format 20*20 à partir de différents board mais le board utilisé pour l'analyse a été plus utilisé pour un peu overfitter le modèle avec un type spécifique de case/piece dessus (mis dans **chess_pieces**)

2) Puis les **pieces ont ete transformées en array de pixels** et **sauvegardées dans un fichier csv** (./dataset/pieces_train.csv et pieces_test.csv) (un de 80% pour le train et un de 20% pour le test). Chaque **premiere case** correspond à un **chiffre qui équivaut à une piece specifique** (ex: 1 => pion blanc). Chaque ligne correspond donc à une image de pièce.

3) Les pieces ont aussi été **détourées** pour pouvoir **reconstituer un board avec des fonds differents** (unique_pieces). Chaque **board** est sauvegardé dans une **ligne de csv** dans **dataset/created_boards**

4) Des **boards** ont ensuite été **simulés** avec les pieces **mises de facon aléatoire et l'arriere plan refait** (created_board)

5) Les **fichiers csv des pieces train** sont donné en entrainement au **Network dans ./classify_board/nn.py**

6) Puis on test le network avec une **image reconstituée** d'un board, redécoupée pour avoir chacune des cases séparément mais pas resauvegardée. **Chaque photo de piece de 20*20** (important) est ensuite **envoyée au Network** qui a été train et qui renvoie une **classification** de la piece de l'image. Apres que chaque case est été analysé **on reconstitue la matrice** renvoyée par le network et on regarde si **elle équivaut** à la ligne correspondante dans le **fichier csv created_boards.csv**.

7) PS: pour tester le **bon learning rate et le bon nombre d'epochs,** on peut les **graphes** crée dans ./graphs. Malheureusement, le **taux de reussit**e reste bas avec un **max de 30%**. On a donc au maximum pour le moment 30% des cases données d'un board qui sont les bonnes, alors que le network s'entraine majoritairement sur les photos de pieces du board en question. (est ce que le **nombre de photos** et donc de data données au network **doit etre le meme pour chaque piece ?** Pour le moment, il y a beaucoup plus de cases blanches/noir et de pion par exemple que de roi => **proportionelle a la possibilité d'avoir telle ou telle piece**)
### Analysis of Stack Overflow (SO) posts on Material Design

This is a simple data analysis on SO posts using Pandas. The goal was to explore the coverage and dynamics of SO posts triggered from the Android Lollipop (5.0) update that introduced Material Design (MD). This was inspired in part by my own frustration with the official documentation when first beginning to implement MD elements, receiving much more guidance from the SO community. I was interested in the idea of *crowd documentation* and what made SO questions/answers better at getting Android developers up to speed on API usage and "gotchas". 

This repo contains the csv files pulled from query results in <a data.stackexchange.com/stackoverflow/query>Stack Overflow Data Exchange</a> and text files containing API changes for Classes/methods, and finally the script that uses the data to analyze posts and prints out descriptive stats.

### Done:

* Answered questions
* Unanswered questions
* Questions with an accepted answer
* Questions with score >= 3
* Questions with votes >= 300
* Questions with favorites
* Questions with links (SO, Android documentation, other)
* Questions which contain images (including gifs) for clarification

### In progress:

* Questions with code markup text for highlighting things like Classes or code samples
* Coverage of the added/changed/removed Classes and methods with the Android 5.0

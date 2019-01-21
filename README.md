# Your Project's Name

The app will randomly take a riddle and answer from a json file, display them to a user and keep track of a leaderbard.

the app is running on python 3 and all logic is contained within.
 
## UX
 
The currently UI is a 3 page design, since column design running on bootstrap. 

## Features

- User log in validation (checked for null values and duplicate user)
- Will validate correct and incorrect user answers.
- Keeps track of a leaderbard which updates on the fly.
- Will allow for multiples uers using different browsers
- The app doesnt handle browser interactions (back button, etc) very well.
- Somethings we get a blow up related to encoding, happens sometimes but needs more investigation.
 

### Features Left to Implement
- Better user input validation (invalid characters, etc)
- setting page allowing a user to add / edit or delete a riddle
- better answer input (currently it needs excate data entry in order to get a correct answer)
- automated testing via cucumber

## Technologies Used

- [python 3](https://www.python.org/download/releases/3.0/)

- [Flask framework](http://flask.pocoo.org/)

- [json](https://www.json.org/)

- [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)

- [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3)

- [Bootstrap](https://getbootstrap.com/)

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.


## Testing

UI elements and text imputs to be aumated via cucumber styles tests (https://cucumber.io/) as well as manual testing. 

AS a new user
WHEN I enter a [Username]
THEN I ecpect to see [Screen]

[Username] - [Screen]
No user name - log in screen with validation message
Duplicate user name - log in screen with calidation message
Valid user name - riddles page

AS A logged in user
AND I an on a riddles page
WHEN I enter a correct answer
THEN I will see the next riddle
AND the leaderbard will update

AS A logged in user
AND I an on a riddles page
WHEN I enter an incorrect answer
THEN I will see the next riddle
AND the leaderbard will update

AS A logged in user
WHEN I open the leaderbard page
THEN I will see a leaderbard


## Deployment

App located on heroku -  https://milstoneproject3-python.herokuapp.com/

no diifference in located and deplyed version

### Content
- all riddles taken from https://riddles.fyi/

### Media
- background image taken from https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQLLsewa9FbKxpHpob4Ty3pFz1buUbnvLBlzRtONxfzBsNnUkl8g

### Acknowledgements

- I received inspiration for this project from X
# Multiplication Practice Game
This is a single-page web game for practicing multiplication facts.
It supports factors 0 through 12.

## Design Constraints
- All code contained in a single page (index.html)
- Use a minimalistic tech stack
  - HTML
  - CSS
  - JavaScript (plus Vue)
  - a sqlite database for storing the log data

## Functionality
- User can/should enter their name in a text box when playing for the first time
- If there is a way to persist the user's name for subsequent sessions, let's do that
- Once user name is established, display a START button
- START begins a session of 10 problems
- User should be able to start typing the answer and hit enter to submit answers. No mouusingg aroundd should be rerquired.
- There should be selectors to set the following options before beginning a session:
  - random problems (default), or practice a specific factor (e.g. 8)
  - normal mode (factors 0-9) or hard mode (factors 0-12)
- Elapsed time between the problem being displayed and the answer being submitted should be logged (but no timer should be displayed)
- Once a session completes, log the following information:
  - session level (session being defined as the set of 10 problems)
    - session_id (UUID)
    - user
    - ip address
    - session start
    - session end
    - session duration (end - start)
  - problem level
    - session_id
    - problem number (1-10)
    - problem (e.g. '8x9')
    - submitted answer
    - correct (boolean)
    - time to solve




## Other Notes
I have an already-running lighttpd server that this will be deployed to.

Basically, every time my daughter plays this game, I want the results to be logged, so I can later
go and perform analysis on her progress in terms of both accuracy and speed.

I'd also like the game to be catchy. By that I mean animations (and sounds if possible) when submitting answers
that make the game a pleasant experience to play.

Stretch goal: It would be cool to have achievements that display fun animations, like 100% correct responses,
a new speed record - things like that.

## lighttpd configuration
Instructions from Claude

```
server.modules += ( "mod_cgi" )
cgi.assign = ( ".py" => "/usr/bin/python3" )
```
Add those two lines to your lighttpd config (typically /etc/lighttpd/lighttpd.conf or a file in /etc/lighttpd/conf.d/). Also make sure the lighttpd process user (often www-data or   
lighttpd) has read/write access to the project directory so it can create/update multiplication_practice.sqlite.

After editing, restart lighttpd:
`sudo systemctl restart lighttpd`
# or
`sudo service lighttpd restart`

Also had to add `".py"` to `static-file.exclude-extensions`

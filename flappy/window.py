# import lib stuff
import pyglet
from pyglet.window import key
from pyglet.gl import *
from pyglet.window import mouse

# import other stuff
from bird import *
from sprites import *

def changeState(state):
    global titleScreenMode
    global highScoreScreenMode
    global gamePlayScreenMode
    global gameOverScreenMode
    global instructionsScreenMode
    global bird_sprite

    if state == 'title':
        titleScreenMode = True
        highScoreScreenMode = False
        gamePlayScreenMode = False
        gameOverScreenMode = False
        instructionsScreenMode = False

    if state == 'highscores':
        titleScreenMode = False
        highScoreScreenMode = True
        gamePlayScreenMode = False
        gameOverScreenMode = False
        instructionsScreenMode = False

    if state == 'gameplay':
        titleScreenMode = False
        highScoreScreenMode = False
        gamePlayScreenMode = True
        gameOverScreenMode = False
        instructionsScreenMode = False

    if state == 'gameover':
        titleScreenMode = False
        highScoreScreenMode = False
        gamePlayScreenMode = False
        gameOverScreenMode = True
        instructionsScreenMode = False
        
    if state == 'instructions':
        titleScreenMode = False
        highScoreScreenMode = False
        gamePlayScreenMode = False
        gameOverScreenMode = False
        instructionsScreenMode = True
        instructionsScreenMode = True


# set up screen transitioning
titleScreenMode = True
highScoreScreenMode = False
gamePlayScreenMode = False
gameOverScreenMode = False
instructionsScreenMode = False
pause = False
gamePlayScreenModeStarted = False

# Set up the current state as the title screen
changeState('title')

# Set up buffer variables
bufferedHeight = 256    
bufferedWidth = 144


#glScalef(2.0, 2.0, 2.0)

# Create the window
window = pyglet.window.Window(bufferedWidth, bufferedHeight, resizable=True)

# TODO: Get the resize event working
@window.event
def on_resize(width, height):
    global titleScreenMode
    global highScoreScreenMode
    global gamePlayScreenMode
    global gameOverScreenMode
    global instructionsScreenMode

    global bufferedHeight, bufferedWidth

    print 'The window was resized to %dx%d' % (width, height)
    glScalef(width / bufferedWidth, height / bufferedHeight, 2.0 ) 

    bufferedHeight = height
    bufferedWidth = width

# Handle the keypress
@window.event
def on_key_press(symbol, modifiers):
    global titleScreenMode
    global highScoreScreenMode
    global gamePlayScreenMode
    global gameOverScreenMode
    global instructionsScreenMode

    if symbol == key.SPACE:
        if gamePlayScreenMode:
            player.bounce_player_game(1)

# Handle mouse presses
@window.event
def on_mouse_press(x, y, button, modifiers):
    global player, gamePlayScreenMode
    print 'The left mouse button was pressed at %d, %d' % (x, y)
    if gamePlayScreenMode:
        player.bounce_player_game(1)

@window.event
def on_mouse_release(x, y, button, modifiers):
    global titleScreenMode
    global highScoreScreenMode
    global gamePlayScreenMode
    global gameOverScreenMode
    global instructionsScreenMode
    global player

    if button == mouse.LEFT:
        print 'The left mouse button was released at %d, %d' % (x, y)
        #pyglet.clock.schedule_interval(player.bounce_player, .05)

    """ Add logic for switching game states """
    if instructionsScreenMode:
        changeState('gameplay')
        print "Changed to gameplay screen"
    if titleScreenMode:
        # Play button logic
        if (x > 21 and x < 60 and y > 63 and y < 75):
            changeState('instructions')
            print "Changed to instuctions screen"
        # Score button logic
        if (x > 80 and x < 119 and y > 63 and y < 75):
            changeState('highscores')
            print "Changed to highscores screen"
        if gamePlayScreenMode:
            pass
        if gameOverScreenMode:
            pass
        if highScoreScreenMode:
            pass

def crash_pipe(sprite):
    global pipe_top_sprite, pipe_bottom_sprite
    return collide([
            pipe_top_sprite1,
            pipe_bottom_sprite1,
            pipe_top_sprite2,
            pipe_bottom_sprite2,
            pipe_top_sprite3,
            pipe_bottom_sprite3,
        ], sprite)

def crash_floor(sprite):
    global bufferedHeight
    return sprite.y > bufferedHeight or sprite.y < 0

def movebg(number):
    global gamePlayScreenMode, bufferedWidth
    if (gamePlayScreenMode):
        background_sprite1.x = background_sprite1.x - 1
        background_sprite2.x = background_sprite2.x - 1
        background_sprite3.x = background_sprite3.x - 1

        pipe_top_sprite1.x = pipe_top_sprite1.x - 2
        pipe_bottom_sprite1.x = pipe_bottom_sprite1.x - 2

        pipe_top_sprite2.x = pipe_top_sprite2.x - 2
        pipe_bottom_sprite2.x = pipe_bottom_sprite2.x - 2

        pipe_top_sprite3.x = pipe_top_sprite3.x - 2
        pipe_bottom_sprite3.x = pipe_bottom_sprite3.x - 2

        if background_sprite1.x <= -bufferedWidth:
            background_sprite1.x = bufferedWidth
        if background_sprite2.x <= -bufferedWidth:
            background_sprite2.x = bufferedWidth
        if background_sprite2.x <= -bufferedWidth:
            background_sprite2.x = bufferedWidth

        if pipe_top_sprite1.x <= -bufferedWidth / 2:
            pipe_top_sprite1.x = bufferedWidth
        if pipe_bottom_sprite1.x <= -bufferedWidth / 2:
            pipe_bottom_sprite1.x = bufferedWidth
        if pipe_top_sprite2.x <= -bufferedWidth / 2:
            pipe_top_sprite2.x = bufferedWidth
        if pipe_bottom_sprite2.x <= -bufferedWidth / 2:
            pipe_bottom_sprite2.x = bufferedWidth
        if pipe_top_sprite3.x <= -bufferedWidth / 2:
            pipe_top_sprite3.x = bufferedWidth
        if pipe_bottom_sprite3.x <= -bufferedWidth / 2:
            pipe_bottom_sprite3.x = bufferedWidth


# Grab fps count
fps_display = pyglet.clock.ClockDisplay()

# Create the player object
player = Bird(bird_animation, 41, 120)
#pyglet.clock.schedule_interval(player.bounce_player, .05)

def schedule_events_to_play():
    global gamePlayScreenModeStarted
    if not gamePlayScreenModeStarted:
        gamePlayScreenModeStarted = True
        pyglet.clock.schedule_interval(player.unbounce_player_game, .007)
        pyglet.clock.schedule_interval(movebg, .005) # update at 60Hz

# Handle the drawing
@window.event
def on_draw():
    global titleScreenMode
    global highScoreScreenMode
    global gamePlayScreenMode
    global gameOverScreenMode
    global instructionsScreenMode

    # Clear the window
    window.clear()
    
    # The following two lines will change how textures are scaled.
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST) 
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # Draw the title screen if nessecary
    if titleScreenMode:
        title_sprite.draw()
    flappybird_sprite.draw()
    bird_sprite.draw()

    # Draw the gameplay screen if nessecary
    if gamePlayScreenMode:
        if crash_floor(player) or crash_pipe(player):
            gamePlayScreenMode = False
            gameOverScreenMode = True
        schedule_events_to_play()
        background_sprite1.draw()
        background_sprite2.draw()
        background_sprite3.draw()
        player.draw()
        pipes_batch.draw()
        

    player.draw_score()
    # Draw the highscore screen if nessecary
    if highScoreScreenMode:
        pass

    # Draw the gameover screen if nessecary
    if gameOverScreenMode:
        pass
    
    # Draw the instructions screen if nessecary
    if instructionsScreenMode:
        instructions_sprite.draw()
	bird_sprite2.draw()
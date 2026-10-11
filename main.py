@namespace
class SpriteKind:
    DeadEnemy = SpriteKind.create()

def on_hit_wall(sprite, location):
    global pound_landed
    if sprite.is_hitting_tile(CollisionDirection.BOTTOM) and ground_pound and not (pound_landed):
        scene.camera_shake(4, 200)
        pound_landed = True
scene.on_hit_wall(SpriteKind.player, on_hit_wall)

def on_a_pressed():
    if playerSprite.is_hitting_tile(CollisionDirection.BOTTOM):
        playerSprite.vy = -300
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

# otherSprite.set_kind(SpriteKind.Other)

def on_on_overlap(sprite2, otherSprite):
    if sprite2.vy > 0 and sprite2.bottom < otherSprite.y:
        if not (ground_pound):
            sprite2.vy = -150
        flattenGoomba(otherSprite)
    else:
        sprite2.say_text("I died!", 5000)
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_on_overlap)

def change_image_on_facing():
    global facing, state
    if not (ground_pound):
        if controller.right.is_pressed():
            facing = "right"
        elif controller.left.is_pressed():
            facing = "left"
        if not (playerSprite.is_hitting_tile(CollisionDirection.BOTTOM)):
            newState = "air-" + facing
        elif controller.left.is_pressed() or controller.right.is_pressed():
            newState = "walk-" + facing
        else:
            newState = "idle-" + facing
        # Only change image/animation when something actually changed
        if newState == state:
            return
        state = newState
        animation.stop_animation(animation.AnimationTypes.ALL, playerSprite)
        if state == "air-right":
            playerSprite.set_image(assets.image("""
                myImage0
                """))
        elif state == "air-left":
            playerSprite.set_image(assets.image("""
                myImage5
                """))
        elif state == "walk-right":
            animation.run_image_animation(playerSprite, walkRight, 100, True)
        elif state == "walk-left":
            animation.run_image_animation(playerSprite, walkLeft, 100, True)
        elif state == "idle-right":
            playerSprite.set_image(assets.image("""
                myImage
                """))
        else:
            playerSprite.set_image(assets.image("""
                myImage6
                """))

def on_down_pressed():
    global ground_pound, pound_landed
    if not (playerSprite.is_hitting_tile(CollisionDirection.BOTTOM)) and not (ground_pound):
        ground_pound = True
        pound_landed = False
        playerSprite.ay = 0
        playerSprite.vy = 0
        controller.move_sprite(playerSprite, 0, 0)
        animation.run_image_animation(playerSprite,
            assets.animation("""
                groundpound_anim
                """),
            30,
            False)
        pause(240)
        animation.stop_animation(animation.AnimationTypes.ALL, playerSprite)
        playerSprite.set_image(assets.image("""
            groundpound
            """))
        playerSprite.vy = 500
        while not (pound_landed):
            pause(1)
        pause(200)  # hold the pose after landing
        ground_pound = False
        controller.move_sprite(playerSprite, 100, 0)
        playerSprite.ay = 500
controller.down.on_event(ControllerButtonEvent.PRESSED, on_down_pressed)

def place_enemies():
    global goombaSprite
    for loc in tiles.get_tiles_by_type(assets.tile("""
        myTile2
        """)):
        enemy_spawns = []
        goombaSprite = sprites.create(assets.image("""
            myImage1
            """), SpriteKind.enemy)
        tiles.place_on_tile(goombaSprite, loc)
        tiles.set_tile_at(loc, assets.tile("""
            transparency16
            """))
        goombaSprite.vx = -25
        goombaSprite.set_bounce_on_wall(True)
        enemy_spawns.append(loc)
def setup():
    global playerSprite
    tiles.set_current_tilemap(tilemap("""
        level1
        """))
    scene.set_background_color(7)
    playerSprite = sprites.create(assets.image("""
        myImage
        """), SpriteKind.player)
    scene.camera_follow_sprite(playerSprite)
    tiles.place_on_tile(playerSprite, tiles.get_tile_location(0, 14))
    tiles.set_tile_at(tiles.get_tile_location(0, 14),
        assets.tile("""
            transparency16
            """))
    controller.move_sprite(playerSprite, 100, 0)
    playerSprite.ay = 500
def flattenGoomba(sprite3: Sprite):
    global projectile
    sprite3.set_kind(SpriteKind.DeadEnemy)
    sprite3.set_image(assets.image("""
        flatGoomba
        """))
    sprite3.lifespan = 1000
    sprite3.vx = 0
    projectile = sprites.create_projectile_from_sprite(img("""
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . 1 . . . 1 . . . 1 . . . .
            . . 1 1 . . 1 . 1 . 1 . 1 . . .
            . . . 1 . . 1 . 1 . 1 . 1 . . .
            . . 1 1 1 . . 1 . . . 1 . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            . . . . . . . . . . . . . . . .
            """),
        sprite3,
        0,
        -20)
    projectile.lifespan = 750
    animation.run_image_animation(projectile,
        assets.animation("""
            scoreAnim
            """),
        100,
        True)
projectile: Sprite = None
goombaSprite: Sprite = None
state = ""
playerSprite: Sprite = None
ground_pound = False
pound_landed = False
facing = ""
walkLeft: List[Image] = []
walkRight: List[Image] = []
walkRight = assets.animation("""
    myAnim
    """)
for frame in walkRight:
    flipped = frame.clone()
    flipped.flip_x()
    walkLeft.append(flipped)
facing = "right"
setup()
place_enemies()

def on_forever():
    change_image_on_facing()
forever(on_forever)

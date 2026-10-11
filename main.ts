namespace SpriteKind {
    export const DeadEnemy = SpriteKind.create()
}
scene.onHitWall(SpriteKind.Player, function (sprite, location) {
    if (sprite.isHittingTile(CollisionDirection.Bottom) && ground_pound && !(pound_landed)) {
        scene.cameraShake(4, 200)
        pound_landed = true
    }
})
controller.A.onEvent(ControllerButtonEvent.Pressed, function () {
    if (playerSprite.isHittingTile(CollisionDirection.Bottom)) {
        playerSprite.vy = -300
    }
})
// otherSprite.set_kind(SpriteKind.Other)
sprites.onOverlap(SpriteKind.Player, SpriteKind.Enemy, function (sprite2, otherSprite) {
    if (sprite2.vy > 0 && sprite2.bottom < otherSprite.y) {
        if (!(ground_pound)) {
            sprite2.vy = -150
        }
        flattenGoomba(otherSprite)
    } else {
        sprite2.sayText("I died!", 5000)
    }
})
function change_image_on_facing () {
    let newState: string;
if (!(ground_pound)) {
        if (controller.right.isPressed()) {
            facing = "right"
        } else if (controller.left.isPressed()) {
            facing = "left"
        }
        if (!(playerSprite.isHittingTile(CollisionDirection.Bottom))) {
            newState = "air-" + facing
        } else if (controller.left.isPressed() || controller.right.isPressed()) {
            newState = "walk-" + facing
        } else {
            newState = "idle-" + facing
        }
        // Only change image/animation when something actually changed
        if (newState == state) {
            return
        }
        state = newState
        animation.stopAnimation(animation.AnimationTypes.All, playerSprite)
        if (state == "air-right") {
            playerSprite.setImage(assets.image`myImage0`)
        } else if (state == "air-left") {
            playerSprite.setImage(assets.image`myImage5`)
        } else if (state == "walk-right") {
            animation.runImageAnimation(
            playerSprite,
            walkRight,
            100,
            true
            )
        } else if (state == "walk-left") {
            animation.runImageAnimation(
            playerSprite,
            walkLeft,
            100,
            true
            )
        } else if (state == "idle-right") {
            playerSprite.setImage(assets.image`myImage`)
        } else {
            playerSprite.setImage(assets.image`myImage6`)
        }
    }
}
controller.down.onEvent(ControllerButtonEvent.Pressed, function () {
    if (!(playerSprite.isHittingTile(CollisionDirection.Bottom)) && !(ground_pound)) {
        ground_pound = true
        pound_landed = false
        playerSprite.ay = 0
        playerSprite.vy = 0
        controller.moveSprite(playerSprite, 0, 0)
        animation.runImageAnimation(
        playerSprite,
        assets.animation`groundpound_anim`,
        30,
        false
        )
        pause(240)
        animation.stopAnimation(animation.AnimationTypes.All, playerSprite)
        playerSprite.setImage(assets.image`groundpound`)
        playerSprite.vy = 500
        while (!(pound_landed)) {
            pause(1)
        }
        pause(200)
        // hold the pose after landing
        ground_pound = false
        controller.moveSprite(playerSprite, 100, 0)
        playerSprite.ay = 500
    }
})
function place_enemies () {
    let enemy_spawns: any[];
for (let loc of tiles.getTilesByType(assets.tile`myTile2`)) {
        enemy_spawns = []
        goombaSprite = sprites.create(assets.image`myImage1`, SpriteKind.Enemy)
        tiles.placeOnTile(goombaSprite, loc)
        tiles.setTileAt(loc, assets.tile`transparency16`)
        goombaSprite.vx = -25
        goombaSprite.setBounceOnWall(true)
        enemy_spawns.push(loc)
    }
}
function setup () {
    tiles.setCurrentTilemap(tilemap`level1`)
    scene.setBackgroundColor(7)
    playerSprite = sprites.create(assets.image`myImage`, SpriteKind.Player)
    scene.cameraFollowSprite(playerSprite)
    tiles.placeOnTile(playerSprite, tiles.getTileLocation(0, 14))
    tiles.setTileAt(tiles.getTileLocation(0, 14), assets.tile`transparency16`)
    controller.moveSprite(playerSprite, 100, 0)
    playerSprite.ay = 500
}
function flattenGoomba (sprite3: Sprite) {
    sprite3.setKind(SpriteKind.DeadEnemy)
    sprite3.setImage(assets.image`flatGoomba`)
    sprite3.lifespan = 1000
    sprite3.vx = 0
    projectile = sprites.createProjectileFromSprite(img`
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
        `, sprite3, 0, -20)
    projectile.lifespan = 750
    animation.runImageAnimation(
    projectile,
    assets.animation`scoreAnim`,
    100,
    true
    )
}
let projectile: Sprite = null
let goombaSprite: Sprite = null
let state = ""
let playerSprite: Sprite = null
let pound_landed = false
let ground_pound = false
let facing = ""
let walkLeft: Image[] = []
let walkRight: Image[] = []
let flipped: Image;
walkRight = assets.animation`myAnim`
for (let frame of walkRight) {
    flipped = frame.clone()
    flipped.flipX()
    walkLeft.push(flipped)
}
facing = "right"
setup()
place_enemies()
forever(function () {
    change_image_on_facing()
})

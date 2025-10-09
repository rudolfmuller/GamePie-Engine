
import gamepie

screen = gamepie.Window(title="Parkour master", flags=gamepie.constants.RESIZABLE,print_fps=True,maximize=True)



count = gamepie.draw.gui.Label(screen,position=(0, 0), font=gamepie.load.Font(size=20),text="Time: null",anti_aliasing=True,background_color=None,visible=True).outline((0, 0, 255), 24)


gamecamera = gamepie.Camera(position=(0, 0), zoom=1, anchor="center")


player_texture = gamepie.load.Texture("plugins:platformassets.textures.jumper")
spike_textures = gamepie.load.Texture("plugins:platformassets.textures.spike")

end_flag_textures = gamepie.load.Texture("plugins:platformassets.textures.end_flag")


player_run = gamepie.load.Frames(r"plugins:platformassets.textures.jumper_go")
player_jump = gamepie.load.Frames(r"plugins:platformassets.textures.jumper_jump")
player_stand = gamepie.load.Frames(r"plugins:platformassets.textures.jumper_stand")
death_sound = gamepie.mixer.Sound(gamepie.load.Audio("plugins:platformassets.textures.jumper_death_sound",volume=10))
jump_sound = gamepie.mixer.Sound(gamepie.load.Audio("plugins:sound.effect.jump"))

player = gamepie.draw.Animation(screen,position=(400 ,-480), frames=player_run,ms=300, size=(45 * 2, 30 * 3), camera=gamecamera,anchor=gamepie.constants.CENTER)

youwin_label = gamepie.draw.gui.Label(screen,position=(2480, -480), font=gamepie.load.Font("DejaVu Sans",50),text="Vyhrál jsi :)",background_color=None,anti_aliasing=True ,camera=gamecamera,anchor=gamepie.constants.TOPLEFT,visible=True).outline((0, 0, 0), 3)

spikes = gamepie.utils.Objects(
    gamepie.draw.Image(screen, texture=spike_textures, position=(380, -73), size=(64, 64), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Image(screen, texture=spike_textures, position=(1850, -380), size=(64, 64), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Image(screen, texture=spike_textures, position=(2250, -380), size=(64, 64), camera=gamecamera, anchor=gamepie.constants.CENTER),

)

map = gamepie.utils.Objects(
    gamepie.draw.Rectangle(screen, position=(-380, 100), size=(200, 30), color=(200, 200, 200), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(-50, 80), size=(120, 25), color=(128,128,128), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(130, 40), size=(120, 25), color=(128, 128, 128), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(380, -40), size=(250, 25), color=(128, 128, 128), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(650, -100), size=(120, 25), color=(128, 128, 128), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(880, -140), size=(140, 25), color=(128, 128, 128), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(1100, -180), size=(120, 30), color=(116, 116, 116), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(1290, -270), size=(120, 30), color=(128, 128, 128), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(1480, -335), size=(120, 30), color=(128, 128, 128), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(1480, -335), size=(260, 30), color=(128, 128, 128), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(1480, -335), size=(260, 30), color=(220, 180, 180), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(1680, -335), size=(120, 30), color=(128, 128, 128), camera=gamecamera, anchor=gamepie.constants.CENTER),
    gamepie.draw.Rectangle(screen, position=(2580, -335), size=(260, 30), color=(220, 180, 180), camera=gamecamera, anchor=gamepie.constants.CENTER),
)
end_block = gamepie.draw.Image(screen,texture=end_flag_textures ,position=(2450, -335), size=(128, 256), camera=gamecamera, anchor=gamepie.constants.BOTTOMLEFT)




controller = gamepie.plugins.Controllers.PlatformController(player=player,camera=gamecamera,gravity=1.5, speed=0.5, jump_power=24, objects=map(),movement_3_key=("left","right","up"))

tck = 0
gamepie.utils.nmsp.set("time",0)
gamepie.utils.nmsp.set("platformBack",0)
def update():
    global tck
    
    dt = screen.fps.tick()
    tck += 1
    controller.update(dt)
    for spike in spikes.all():
        
        if spike.collision.rect(player,offset=(32, 0,-48, 0)) or player.y >= 500:
            player.color = (255,0,0)
            player.pos =(-400, 100)
            gamepie.utils.nmsp.set("time", 0)
            death_sound.play()
    if controller.status == "right":
        player.flip = (False,False)
        player.animation = player_run
        player.play()
    elif controller.status == "left":
        player.flip = (True,False)
        player.animation = player_run
        player.play()
    elif controller.status == "jump":
        if gamepie.wait(600,f"PlayerJumpSound.{id(map()[6])}:S"):jump_sound.play()
        player.animation = player_jump
        player.play()
    elif controller.status == "falling":
        player.animation = player_jump
        player.play()
    else:
        player.animation = player_stand
        player.play()
        

    if gamepie.wait(500,f"SwitchBlock.{id(map()[6])}:<"):
        map()[6].enable = True
    elif gamepie.wait(1000,f"SwitchBlock.{id(map()[6])}:>"):
        map()[6].enable = False
    if not map()[12].collision.rect(player):
        gamepie.utils.nmsp.set("time", gamepie.utils.nmsp.get("time") + 1)
        
    if gamepie.wait(500,f"PlayerKillColor.{id(map()[6])}:Normal"):player.color = (255,255,255) 
    platform = map()[11]  
    if not gamepie.utils.nmsp()["platformBack"]: 
        platform.x += 3
        if platform.x >= 2580:
            gamepie.utils.nmsp.set("platformBack" ,True)
    else: 
        platform.x -= 3
        if platform.x <= 1680:
            gamepie.utils.nmsp.set("platformBack" ,False)
    screen.fill(gamepie.color.mycolor("sky-lx3"))
    count.text = f"Time: {gamepie.utils.nmsp().get('time')}"
    youwin_label.draw()
    player.draw()
    spikes.draw()
    map.draw()
    end_block.draw()
    count.draw()
    

    screen.flip()

screen.run()
gamepie.quit()

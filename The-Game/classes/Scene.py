#Import basic librairies
import pyglet
from pyglet.gl import *
#Import personal packages
from constants import constants
from classes import Sprite, Player, Event, Deco

class Scene_de_theatre(object):

    def __init__(self, my_theatre, my_piece, my_scene):

        #info - - - - - - - - - - - - - - - - - - - - - - 
        print("scene creation : ", my_scene)
        #global variables - - - - - - - - - - - - - - - - 
        self.run = True
        self.name = my_scene
        self.new_name = self.name
        #player - - - - - - - - - - - - - - - - - - - - - 
        self.player_pos = [320, 480]
        self.player_sprite = None
        #theatre- - - - - - - - - - - - - - - - - - - - - 
        self.my_theatre = my_theatre
        self.my_piece = my_piece
        self.my_scene = my_scene
        #event and batch- - - - - - - - - - - - - - - - - 
        #self.my_event = Event.Event()
        self.event_list = []
        self.batch = pyglet.graphics.Batch()
        #sprite lists - - - - - - - - - - - - - - - - - - 
        self.sprite_list = []
        self.sprite_list_collidable = []

        #LAUNCH SCENE = = = = = = = = = = = = = = = = = = 
        self.my_scene_is_loaded = False
        self.load_scene()
        self.my_scene_is_loaded = True
        # = = = = = = = = = = = = = = = = = = = = = = = =

        #object finalisation- - - - - - - - - - - - - - - 
        self.player_sprite.sprite_list = self.sprite_list
        self.player_sprite.sprite_list_collidable = self.sprite_list_collidable
        self.player_sprite.textbox = self.textbox_sprite

        #info - - - - - - - - - - - - - - - - - - - - - - 
        print("Number of sprites: ", len(self.sprite_list))
        print("Number of collidable sprites: ", len(self.sprite_list_collidable))
        
  
    def load_scene(self):

        self.load_my_scene()


    def load_my_scene(self):
        
        self.sprite_list = []
        self.load_background()
        minimap = self.load_tiles()
        self.load_deco(minimap)
        self.load_events(minimap)
        self.load_textbox()
        self.load_player()
        #self.load_frontground()
        self.load_HUD()
        self.load_camera()

        for sprite in self.sprite_list:
            if sprite.collidable:
               self.sprite_list_collidable.append(sprite)
               

    def load_background(self):

        my_scene = self.my_scene
        
        base = constants.PATH_BACK + constants.BASE_BACK_STYLE[my_scene] + ".png"
        base_z = pyglet.graphics.OrderedGroup(0)
        base_image = pyglet.image.load(base)
        self.anti_aliasied_texture(base_image)
        base_sprite = Sprite.New_sprite(base_image, 0, 0, 0, constants.SPRITE_X, constants.SPRITE_Y, my_batch = self.batch, my_group = base_z, spr_type = "base", collidable = False, my_scene = my_scene)
        self.sprite_list.append(base_sprite)

        back_list = constants.BACK_STYLE[my_scene]
        back_sprite_list = []
        for back_id in range(len(back_list)):
            back = constants.PATH_BACK + constants.BACK_STYLE[my_scene][back_id] + ".png"
            back_z = pyglet.graphics.OrderedGroup(back_id + 2)
            back_image = pyglet.image.load(back)
            self.anti_aliasied_texture(back_image)
            for i in range(2):
                back_sprite = Sprite.New_sprite(back_image, constants.SCREEN_X*i, 0, back_id + 1, constants.SPRITE_X, constants.SPRITE_Y, my_batch = self.batch, my_group = back_z, spr_type = "back", collidable = False, my_scene = my_scene)
                self.sprite_list.append(back_sprite)
    
    
    def load_tiles(self):
        
        my_scene = self.my_scene

        tileset_path = constants.PATH_TILE+ constants.TILE_STYLE[my_scene] + ".png"
        tile_z = pyglet.graphics.OrderedGroup(100)
        tileset_image = pyglet.image.load(tileset_path)
        self.anti_aliasied_texture(tileset_image)
        nb_tile_col = int(tileset_image.width/constants.SPRITE_X)
        nb_tile_row = int(tileset_image.height/constants.SPRITE_Y)
        tile_image_list_32px = pyglet.image.ImageGrid(tileset_image, nb_tile_row, nb_tile_col)
        tile_image_list_64px = pyglet.image.ImageGrid(tileset_image, int(nb_tile_row/2), nb_tile_col)
        tile_image_list = [None] * (nb_tile_col *nb_tile_row)

        tile_image_list[:4] = tile_image_list_64px[:4]
        tile_image_list[4:16] = tile_image_list_32px[4:16]
        tile_image_list[16:20] = tile_image_list_64px[8:]
        tile_image_list[20:] = tile_image_list_32px[20:]
        
        minimap = constants.PATH_MAP + constants.MAP_STYLE[my_scene] + ".png"
        minimap_image = pyglet.image.load(minimap)
        minimap_data = minimap_image.get_image_data()
        minimap_pixels = minimap_data.get_data('RGB', minimap_image.width * 3)
        minimap_array = [[None for x in range(minimap_image.width)] for y in range(minimap_image.height)]
        
        for y in range(minimap_image.height):
            for x in range(minimap_image.width):
                pix_pos = (x + y * minimap_image.width)*3
                r = int(str(minimap_pixels[pix_pos]))
                g = int(str(minimap_pixels[pix_pos+1]))
                b = int(str(minimap_pixels[pix_pos+2]))
                minimap_array[y][x] = [r, g, b]

        complete_tile = False
        tile_length = 0
        ID_tile_list = []
        for y in range(minimap_image.height):
            complete_tile = False
            tile_length = 0
            ID_tile_list = []
            for x in range(minimap_image.width):
                
                if minimap_array[y][x] == [0, 0, 0]:
                    if tile_length == 0:
                        complete_tile = False
                    tile_length += 1
                    ID = self.load_tiles_get_ID(minimap_array, x, y)
                    ID_tile_list.append(ID)
                else:
                    complete_tile = True
                    
                if x == minimap_image.width - 1:
                    complete_tile = True
                    
                if complete_tile and tile_length > 0:
                    tile_x = (x-tile_length) * constants.SPRITE_X
                    tile_y = y * constants.SPRITE_Y
                    my_batch = self.get_batch()
                    #ID = self.load_tiles_get_ID(minimap_array, x-tile_length, y)
                    collidable = True
                    self.anti_aliasied_texture(tile_image_list[ID])
                    tile_length = constants.SPRITE_X * tile_length
                    tile_height = constants.SPRITE_Y
                    tile_image = pyglet.image.Texture.create(tile_length, tile_height*2)
                    my_local_x = 0
                    for ID in ID_tile_list:
                        tile_image.blit_into(tile_image_list[ID], my_local_x, 0, 0)
                        my_local_x += constants.SPRITE_X
                    tile_sprite = Sprite.New_sprite(tile_image, tile_x, tile_y, 100, tile_length, tile_height, my_batch = my_batch, my_group = tile_z, spr_type = "tile", collidable = collidable, my_scene = my_scene)
                    self.sprite_list.append(tile_sprite)
                    complete_tile = False
                    tile_length = 0
                    ID_tile_list = []
                    
        return minimap_array

    
    def load_deco(self, minimap_array):

        my_scene = self.my_scene

        deco_object = Deco.Deco()
        deco_info = deco_object.get_deco(my_scene)

        deco_sprite_info = []
        
        for y in range(self.get_minimap_height(my_scene)):
            for x in range(self.get_minimap_width(my_scene)):
                
                ID = self.get_deco_id_from_color(minimap_array[y][x])
                is_deco = False
                
                for deco_id in range(len(deco_info)):
                    if deco_info[deco_id][0] == ID:
                        is_deco = True
                        ID = deco_id

                if is_deco: #deco ID  (001b to 111b)

                    deco_sprite_info = deco_info[ID]
                    
                    deco = constants.PATH_DECO + deco_sprite_info[1] + ".png"
                    my_x = (x + deco_sprite_info[7]) * constants.SPRITE_X
                    my_y = (y + deco_sprite_info[8]) * constants.SPRITE_Y
                    my_y_original = my_y
                    my_z = deco_sprite_info[3]
                    deco_z = pyglet.graphics.OrderedGroup(my_z)
                    deco_collidable = deco_sprite_info[6]
                    deco_image = pyglet.image.load(deco)
                    self.anti_aliasied_texture(deco_image)
                    
                    if deco_sprite_info[2] > 0:
                        my_y += (-1) * deco_sprite_info[2] * deco_image.height + constants.SPRITE_Y

                    if my_y < 0:
                        y_cut = 0
                        x_cut = 0
                        h_cut = my_y_original + constants.SPRITE_X
                        w_cut = deco_image.width
                        deco_image = deco_image.get_region(x_cut, y_cut, w_cut, h_cut)
                        my_y = 0
                                                
                    if deco_sprite_info[4]: #animated ?
                        nb_frame = int(deco_image.width/constants.SPRITE_X)
                        speed = deco_sprite_info[5]
                        loop = True
                        deco_image_sequence = pyglet.image.ImageGrid(deco_image, 1, nb_frame)
##                        offset = x % nb_frame
##                        sequence_tmp = []
##                        for img in deco_image_sequence:
##                            sequence_tmp.append(deco_image_sequence[offset])
##                            offset += 1
##                            if offset >= nb_frame: offset = 0
##                            self.anti_aliasied_texture(img)
##
##                        deco_image_sequence = sequence_tmp   
                        deco_image = pyglet.image.Animation.from_image_sequence(deco_image_sequence, speed, loop)
                    else:
                        self.anti_aliasied_texture(deco_image)
                    deco_sprite = Sprite.New_sprite(deco_image, my_x, my_y, my_z, constants.SPRITE_X, constants.SPRITE_Y, my_batch = self.batch, my_group = deco_z, spr_type = "deco", collidable = deco_collidable, my_scene = my_scene)

                    self.sprite_list.append(deco_sprite)

    
    def load_events(self, minimap_array):

        my_scene = self.my_scene

        event_object = Event.Event()
        event_info = event_object.get_event(my_scene)

        event_sprite_info = []
        
        for y in range(self.get_minimap_height(my_scene)):
            for x in range(self.get_minimap_width(my_scene)):
                
                ID = self.get_deco_id_from_color(minimap_array[y][x])
                is_event = False
                
                for event_id in range(len(event_info)):
                    if event_info[event_id][0] == ID:
                        is_event = True
                        ID = event_id

                if is_event: #event ID  (001b to 111b)
                    event_sprite_info = event_info[ID]
                    
                    event = constants.PATH_EVENT + event_sprite_info[1] + ".png"
                    my_x = (x + event_sprite_info[7]) * constants.SPRITE_X
                    my_y = (y + event_sprite_info[8]) * constants.SPRITE_Y
                    my_y_original = my_y
                    my_z = event_sprite_info[3]
                    event_z = pyglet.graphics.OrderedGroup(my_z)
                    event_collidable = event_sprite_info[6]
                    event_image = pyglet.image.load(event)
                    self.anti_aliasied_texture(event_image)
                    
                    if event_sprite_info[2] > 0:
                        my_y += (-1) * event_sprite_info[2] * event_image.height + constants.SPRITE_Y

                    if my_y < 0:
                        y_cut = 0
                        x_cut = 0
                        h_cut = my_y_original + constants.SPRITE_X
                        w_cut = event_image.width
                        event_image = event_image.get_region(x_cut, y_cut, w_cut, h_cut)
                        my_y = 0
                                                
                    if event_sprite_info[4]: #animated ?
                        nb_frame = int(event_image.width/constants.SPRITE_X)
                        speed = event_sprite_info[5]
                        loop = True
                        event_image_sequence = pyglet.image.ImageGrid(event_image, 1, nb_frame)
                        offset = x % nb_frame
                        sequence_tmp = []
                        for img in event_image_sequence:
                            sequence_tmp.append(event_image_sequence[offset])
                            offset += 1
                            if offset >= nb_frame: offset = 0
                            self.anti_aliasied_texture(img)

                        event_image_sequence = sequence_tmp   
                        event_image = pyglet.image.Animation.from_image_sequence(event_image_sequence, speed, loop)
                    else:
                        self.anti_aliasied_texture(event_image)
                    event_sprite = Sprite.New_sprite(event_image, my_x, my_y, my_z, constants.SPRITE_X, constants.SPRITE_Y, my_batch = self.batch, my_group = event_z, spr_type = "event", collidable = event_collidable, my_scene = my_scene)

                    self.sprite_list.append(event_sprite)
                    self.event_list.append([event_sprite_info, event_sprite])


    def load_textbox(self):
        
        my_scene = self.my_scene
        textbox_batch = self.batch
        
        textbox = constants.PATH_TEXTBOX + "000.png"
        textbox_z = pyglet.graphics.OrderedGroup(900)
        textbox_image = pyglet.image.load(textbox)
        self.anti_aliasied_texture(textbox_image)
        self.textbox_sprite = Sprite.New_sprite(textbox_image, 0, 0, 0, constants.SPRITE_X, constants.SPRITE_Y, my_batch = textbox_batch, my_group = textbox_z, spr_type = "textbox", collidable = False, my_scene = my_scene)
        self.sprite_list.append(self.textbox_sprite)

             
    def load_player(self):
        
        my_scene = self.my_scene

        player_z = pyglet.graphics.OrderedGroup(400)
        self.player_sprite = Player.Player_sprite(self.player_pos[0], self.player_pos[1], 400, my_batch = self.batch, my_group = player_z, spr_type = "player", collidable = False, my_scene = my_scene, my_event_list = self.event_list)

        self.sprite_list.insert(0, self.player_sprite)

    
    def load_frontground(self):
        
        my_scene = self.my_scene
        
        front = constants.PATH_FRONT + constants.FRONT_STYLE[my_scene] + ".png"
        front_z = pyglet.graphics.OrderedGroup(800)
        front_image = pyglet.image.load(front)
        self.anti_aliasied_texture(front_image)
        front_batch = self.batch
        front_sequence = pyglet.image.ImageGrid(front_image, 1, 4)
        front_animation = pyglet.image.Animation.from_image_sequence(front_sequence, 0.25, True)
        front_sprite = Sprite.New_sprite(front_animation, 0, 0, 0, constants.SPRITE_X, constants.SPRITE_Y, my_batch = front_batch, my_group = front_z, spr_type = "front", collidable = False, my_scene = my_scene)
        self.sprite_list.append(front_sprite)

        ambiance = constants.PATH_FRONT + "003" + ".png"
        ambiance_z = pyglet.graphics.OrderedGroup(799)
        ambiance_image = pyglet.image.load(ambiance)
        self.anti_aliasied_texture(ambiance_image)
        ambiance_batch = self.batch
        ambiance_sprite = Sprite.New_sprite(ambiance_image, 0, 0, 0, constants.SPRITE_X, constants.SPRITE_Y, my_batch = ambiance_batch, my_group = ambiance_z, spr_type = "front", collidable = False, my_scene = my_scene)
        self.sprite_list.append(ambiance_sprite)
        

    def load_HUD(self):

        my_scene = self.my_scene
        
        fps = str(pyglet.clock.get_fps())
        
        number_sheet = constants.PATH_HUD + "008" + ".png"
        hud_batch = self.batch
        number_z = pyglet.graphics.OrderedGroup(900)
        number_sheet_image = pyglet.image.load(number_sheet)
        number_list = pyglet.image.ImageGrid(number_sheet_image, 1, 10)
    
        for num in range(4):
            number_sprite = Sprite.New_sprite(number_list[0], 2+num*7, 460, 900, constants.SPRITE_X, constants.SPRITE_Y, my_batch = hud_batch, my_group = number_z, spr_type = "fps_" + str(num), collidable = False, my_scene = my_scene)
            self.sprite_list.append(number_sprite)


    def load_camera(self):

        self.camera_target = self.player_sprite

        
    def key_pressed(self, key, modifiers):

        self.player_sprite.key_pressed(key, modifiers)
        

    def key_released(self, key, modifiers):

        self.player_sprite.key_released(key, modifiers)
        

    def update(self, dt):

        if self.new_name != self.name:
            self.name = self.new_name
            self.delete_all_sprites()
            self.run = False
            self.my_piece.change_scene(self.new_name)

        if self.run:

            self.sprite_list_collidable = []
            
            for sprite in self.sprite_list:
                    sprite.update(self.sprite_list, dt, self.player_sprite)
                    if sprite.visible and sprite.collidable:
                        self.sprite_list_collidable.append(sprite)

            self.player_sprite.sprite_list_collidable = self.sprite_list_collidable
            
            self.update_camera()
        
            
    def update_camera(self):

        if self.my_scene != "LEVEL_SELECT":
            glMatrixMode(GL_PROJECTION);
            glLoadIdentity();
            glOrtho(self.camera_target.x-constants.SCREEN_X/2, self.camera_target.x+constants.SCREEN_X/2, 0, 480, 0, 1);
        else:
            glMatrixMode(GL_PROJECTION);
            glLoadIdentity();
            glOrtho(0, constants.SCREEN_X, 0, 480, 0, 1);
          

    def delete_all_sprites(self):
        
        for sprite in self.sprite_list:
            sprite.delete()


    def get_minimap_width(self, my_scene):
        
        minimap = constants.PATH_MAP + constants.MAP_STYLE[my_scene] + ".png"
        minimap_image = pyglet.image.load(minimap)
        return minimap_image.width


    def get_minimap_height(self, my_scene):
        
        minimap = constants.PATH_MAP + constants.MAP_STYLE[my_scene] + ".png"
        minimap_image = pyglet.image.load(minimap)
        return minimap_image.height
    

    def get_batch(self):
        
        return self.batch
    

    def get_deco_id_from_color(self, color):

        r = color[0]
        g = color[1]
        b = color[2]
        ID = -1

        if r == 0 or r == 100 or r == 200:
            if g == 0 or g == 100 or g == 200:
                if b == 0 or b == 100 or b == 200:
                    if r + g + b > 0:
                        r = int(r/100)
                        g = int(g/100)
                        b = int(b/100)
                        ID = 9*r + 3*g + 1*b

        return ID
    

    def load_tiles_get_ID(self, minimap, x, y):
       
        if y+1 < len(minimap) and minimap[y+1][x] != [0,0,0]:
            
            if y-1 >= 0 and minimap[y-1][x] != [0,0,0]:
                if x+1 < len(minimap[y]) and minimap[y][x+1] != [0,0,0]:
                    if x-1 >= 0 and minimap[y][x-1] != [0,0,0]:
                        return 3
                    else:
                        return 2
                elif x-1 >= 0 and minimap[y][x-1] != [0,0,0]:
                    return 0
                else:
                    return 1
                
            elif x+1 < len(minimap[y]) and minimap[y][x+1] != [0,0,0]:
                if x-1 >= 0 and minimap[y][x-1] != [0,0,0]:
                    return 19
                else:
                    return 18
            elif x-1 >= 0 and minimap[y][x-1] != [0,0,0]:
                return 16
            else:
                return 17
            
        elif y-1 >= 0 and minimap[y-1][x] != [0,0,0]:
            if x+1 < len(minimap[y]) and minimap[y][x+1] != [0,0,0]:
                if x-1 >= 0 and minimap[y][x-1] != [0,0,0]:
                    return 11
                else:
                    return 10
            elif x-1 >= 0 and minimap[y][x-1] != [0,0,0]:
                return 8
            else:
                return 9
            
        elif x+1 < len(minimap[y]) and minimap[y][x+1] != [0,0,0]:
            if x-1 >= 0 and minimap[y][x-1] != [0,0,0]:
                return 15
            else:
                return 14
        elif x-1 >= 0 and minimap[y][x-1] != [0,0,0]:
            return 12
        else:
            return 13


    def anti_aliasied_texture(self, img):
        
        texture = img.get_texture()
        glBindTexture(texture.target, texture.id)
        glTexParameteri(texture.target,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
        glBindTexture(texture.target,0)

        

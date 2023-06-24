from lib.style import *

def init(m):
    if m.hasLoadedGallery == False:
        m.galleryImages = []

        m.galleryImagesList = m.file_list('camera/')

        for img in m.galleryImagesList:
            image = pygame.image.load('./data/fs/camera/' + img).convert()
            image = pygame.transform.scale(image, (100, 100))
            m.galleryImages.append(image)
        
        m.hasLoadedGallery = True
    

def gallery(m):
    global xIndex
    global yIndex
    initApp(m)

    scroll_box()  

    #* CONTENT

    titleBar('Gallery', color=BLUE)
    set_direction('y')

    # IMAGES
    
    if m.hasLoadedGallery == True:
        for img in m.galleryImages:
            image('../data/fs/camera/', size=(100, 100), raw=img, needsScaling=False)

    #! END OF CONTENT

    end_scroll_box()
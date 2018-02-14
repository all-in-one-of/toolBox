
# script to do

# screenShot flipbook : y.screenShot bloque
#y.render set un node mantra 
# merge la geo selection dans un nouveau node qui sera linker au node mantra
# sauvegarde toutes les previz du render view: y.previzSave // tricky
# set up de shading avec shading ball et environment : y.shadingBall y.123


print ("---- Bonjour Michael ! ----")

print ("***for help type: help(y) ***")

def manual():
    
    """setup scene to manual mode
    """
    help(manual)

    import hou
    mode = hou.updateModeSetting().name()
    if mode == 'AutoUpdate':
        hou.setUpdateMode(hou.updateMode.Manual)
    if mode == 'Manual':
        hou.setUpdateMode(hou.updateMode.AutoUpdate)

def unDeuxTrois():

    """ setup une start scene basique
    """
   
    help(unDeuxTrois)   

    import hou
    obj = hou.node("/obj")

    cam = obj.createNode("cam","myCam")
    cam.setParms({"resx":1920,"resy":1080})
    cam.setParms({"tz":3,"ty":1.7})

    resSim = obj.createNode("null","resSim")
    resSim.setDisplayFlag(False)

    parm_group = resSim.parmTemplateGroup()
    parm_folder = hou.FolderParmTemplate("folder","resSim")
    parm_folder.addParmTemplate(hou.FloatParmTemplate("flipSim","flipSim",1))
    parm_folder.addParmTemplate(hou.FloatParmTemplate("pyroSim","pyroSim",1))
    parm_group.append(parm_folder)
    resSim.setParmTemplateGroup(parm_group)



    geo1 = obj.createNode ("geo","source")
    geo1.move([0, -2])
    file1 = hou.node("/obj/source/file1")
    file1.destroy()
      
    env = obj.createNode("envlight","myEnv")
    env.setParms ({"env_map":"$HFS/houdini/pic/DOSCH_SKIESV2_01SN_lowres.rat"})  
    env.move([0, 1])

    out = hou.node("/out")
    mantra = out.createNode("ifd","myMantra")
    mantra.setParms({"vm_renderengine":"pbrraytrace","camera":"/obj/myCam"})

    shop = hou.node("/shop")
    mat = shop.createNode("principledshader","myMat")
    mat.setParms({"basecolorr":1,"basecolorg":1,"basecolorb":1}) 


def quatreCinqSix():

    """ set the houdini desktop 
    """

    help(quatreCinqSix)

    import hou

    #decrire la configuration du desktop avec python
    # close treeView close python open spreadsheet,chage parameter to python 
    desktops_dict = dict((d.name(), d) for d in hou.ui.desktops())
    desktops_dict['Technical2'].setAsCurrent()
	
    mode = hou.updateModeSetting().name()
    if mode == 'AutoUpdate':
        hou.setUpdateMode(hou.updateMode.Manual)



def bound():

    """return bound box and centroid"""

    help(bound)

    import hou
    nodeSelect = hou.selectedNodes()
    black=hou.Color((0,0,0))
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        getName = node.name()
        outNull = node.createOutputNode("null",getName+"_IN_BOUND")
        outNull.setPosition(node.position())
        outNull.move([0, -1])
        outNull.setColor(black)
        outBound= outNull.createOutputNode("null",getName+"_BOUND_CENTROID")
        outBound.setColor(pink)
        #add create param to outBound
        parm_group = outBound.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("folder","Bound_Centroid")
        parm_folder.addParmTemplate(hou.FloatParmTemplate("bound","Bound",3))
        parm_folder.addParmTemplate(hou.FloatParmTemplate("centroid","Centroid",3))
        parm_group.append(parm_folder)
        outBound.setParmTemplateGroup(parm_group)

        outBound.parm('boundx').setExpression("bbox(opinputpath('.',0),D_XSIZE)")
        outBound.parm('boundy').setExpression("bbox(opinputpath('.',0),D_YSIZE)")
        outBound.parm('boundz').setExpression("bbox(opinputpath('.',0),D_ZSIZE)")

        outBound.parm('centroidx').setExpression("centroid(opinputpath('.',0),D_X)")
        outBound.parm('centroidy').setExpression("centroid(opinputpath('.',0),D_Y)")
        outBound.parm('centroidz').setExpression("centroid(opinputpath('.',0),D_Z)")


def rotTool():

    """
    help rotate scatter with orient attribute
    """
    help(rotTool)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","rotTool")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""

matrix myTransform= maketransform(0,0,chv("t"),chv("r"),chv("s"),chv("p")); // translate rotate scale pivot
@orient = quaternion(matrix3(myTransform)); 

"""}) 
        print("--- Don't forget create channels parameter in the wrangle node ---")

def normalizeGeoYVex ():

    """
    normalize the size of the geo and move it to zero
    """
    help(normalizeGeoYVex)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","normalizeGeoVexByHeight")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
//center geo
vector min, max;
getbbox(0, min, max);
vector centroid = (min+max)/2;;
@P+= centroid*-1;

@P*= 1/(max.y-min.y); //normalize by max height 
@P.y+=0.5; //normalize by max height

@P*=ch('realScale'); //real scale"""}) 
        print("--- Don't forget to just clic for create channels param in the wrangle node ---")

def normalizeGeoMaxSize ():

    """
    normalize by max size and centroid
    """
    help(normalizeGeoMaxSize)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","normalizeGeoVexByHeight")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
//center geo
vector min, max;
getbbox(0, min, max);
vector centroid = (min+max)/2;;
@P+= centroid*-1;

@P*= 1/(max(max.x-min.x,max.y-min.y,max.z-min.z)); //normalize by max size
@P*=2;"""}) 
        





def cacheBgeo ():

    """ cree un rop output dans /out et le recharge dans le context d'origine
    cela permet d'enchainer les depandences dans /out et de les relires automatiquement
    dans dans le contexte d'origine
    """

    help(cacheBgeo)

    import hou
    nodeSelect = hou.selectedNodes()
    black=hou.Color((0,0,0))
    pink=hou.Color((0.98,0.275,0.275))
    out= hou.node("/out")

    for node in nodeSelect:
        parent = node.parent()  #hou.node("..")
        parentString =parent.name()    
        getName = node.name()
        connectNode = node.outputs()
        outNull = node.createOutputNode("null",getName.upper())
        outNull.setPosition(node.position())
        outNull.move([0, -.75])
        outNull.setColor(black)

        #set read node to read myWriteGeo
        myFile = outNull.createOutputNode("file",getName.upper()+"_CACHE")
        myFile.setColor(pink)
        myFile.setParms({'file': '$HIP/cache/rop_sfx/bgeo.sc/$OS/v`padzero(3,chs("/out/$OS/version"))`/$OS.$F5.bgeo.sc'})
        myWriteGeo= out.createNode("geometry",getName.upper()+"_CACHE")
        myWriteGeo.setParms({"soppath":"/obj/"+parentString+"/"+getName.upper()})
        myWriteGeo.setParms({"sopoutput":"$HIP/cache/rop_sfx/bgeo.sc/$OS/v`padzero(3, ch('version'))`/$OS.$F5.bgeo.sc"})
        myWriteGeo.setParms({"trange":"normal"})

        #add create param for versionning and export format
        parm_group = myWriteGeo.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("folder","version")
        parm_folder.addParmTemplate(hou.IntParmTemplate("version","Version",1))
        parm_group.append(parm_folder)
        myWriteGeo.setParmTemplateGroup(parm_group)


def cacheVdb ():

    """ cree un rop output dans /out et le recharge dans le context d'origine
    cela permet d'enchainer les depandences dans /out et de les relires automatiquement
    dans dans le contexte d'origine
    """

    help(cacheVdb)

    import hou
    nodeSelect = hou.selectedNodes()
    black=hou.Color((0,0,0))
    pink=hou.Color((0.98,0.275,0.275))
    out= hou.node("/out")

    for node in nodeSelect:
        parent = node.parent()  #hou.node("..")
        parentString =parent.name()    
        getName = node.name()
        connectNode = node.outputs()
        outNull = node.createOutputNode("null",getName.upper())
        outNull.setPosition(node.position())
        outNull.move([0, -.75])
        outNull.setColor(black)

        #set read node to read myWriteGeo
        myFile = outNull.createOutputNode("file",getName.upper()+"_CACHE")
        myFile.setColor(pink)
        myFile.setParms({'file': '$HIP/cache/rop_sfx/vdb/$OS/v`padzero(3,chs("/out/$OS/version"))`/$OS.$F5.vdb'})
        myWriteGeo= out.createNode("geometry",getName.upper()+"_CACHE")
        myWriteGeo.setParms({"soppath":"/obj/"+parentString+"/"+getName.upper()})
        myWriteGeo.setParms({"sopoutput":"$HIP/cache/rop_sfx/vdb/$OS/v`padzero(3, ch('version'))`/$OS.$F5.vdb"})
        myWriteGeo.setParms({"trange":"normal"})

        #add create param for versionning
        parm_group = myWriteGeo.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("folder","version")
        parm_folder.addParmTemplate(hou.IntParmTemplate("version","Version",1))
        parm_group.append(parm_folder)
        myWriteGeo.setParmTemplateGroup(parm_group)

def cacheAbc ():

    """ cree un rop output dans /out et le recharge dans le context d'origine
    cela permet d'enchainer les depandences dans /out et de les relires automatiquement
    dans dans le contexte d'origine
    """

    help(cacheAbc)

    import hou
    nodeSelect = hou.selectedNodes()
    black=hou.Color((0,0,0))
    pink=hou.Color((0.98,0.275,0.275))
    out= hou.node("/out")

    for node in nodeSelect:
        parent = node.parent()  #hou.node("..")
        parentString =parent.name()    
        getName = node.name()
        connectNode = node.outputs()
        outNull = node.createOutputNode("null",getName.upper())
        outNull.setPosition(node.position())
        outNull.move([0, -.75])
        outNull.setColor(black)

        #set read node to read myWriteGeo
        myFile = outNull.createOutputNode("alembic",getName.upper()+"_CACHE")
        myFile.setColor(pink)
        myFile.setParms({'fileName': '$HIP/cache/rop_sfx/abc/$OS/v`padzero(3,chs("/out/$OS/version"))`/$OS.abc'})
        #set write geo in out context
        myWriteGeo=out.createNode("alembic",getName.upper()+"_CACHE")
        #set parm
        myWriteGeo.setParms({"use_sop_path":1})
        myWriteGeo.setParms({"sop_path":"/obj/"+parentString+"/"+getName.upper()})
        myWriteGeo.setParms({"filename":"$HIP/cache/rop_sfx/abc/$OS/v`padzero(3, ch('version'))`/$OS.abc"})
        myWriteGeo.setParms({"trange":"normal"})
        #add create param for versionning
        parm_group = myWriteGeo.parmTemplateGroup()
        versionParm =hou.IntParmTemplate("version","Version",1)
        target_folder = ("Main")
        parm_group.appendToFolder(target_folder,versionParm)
        myWriteGeo.setParmTemplateGroup(parm_group)
        


def pywy ():

    """
    create a node to test code with python
    """

    help(pywy)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        #create node from selected node
        pyNull = node.createOutputNode("null","pythonRunCode")
        pyNull.setColor(pink)
        #prepa param
        parm_group = pyNull.parmTemplateGroup()
        parm_folder = hou.FolderParmTemplate("folder","pywy")
        #button run code
        button=hou.ButtonParmTemplate("runcode","Run_Code")
        button.setTags({"script_callback_language":"python","script_callback":"exec(kwargs['node'].parm('pythonCode').eval())"})
        parm_folder.addParmTemplate(button)
        #multistring
        multistring=hou.StringParmTemplate("pythonCode","PythonCode",1)         
        multistring.setTags({"editor":"1","editorlang":"python"})
        parm_folder.addParmTemplate(multistring)
        #append param
        parm_group.append(parm_folder)
        pyNull.setParmTemplateGroup(parm_group)



def camUvDelete ():

    """
    delete geo by camera range
    """
    help(camUvDelete)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","camUvDelete")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
vector ndc=toNDC(chs("camPath"),@P);
@Cd = ndc; // viz
float secu = 0.1;
if(ndc.x+secu<0||ndc.x-secu>1||ndc.y+secu<0||ndc.y-secu>1||ndc.z>1){
removepoint(geoself(),@ptnum);
}"""}) 
        print("--- Don't forget to check the campath in camUvdelete ---")

def camUvDeleteAnim ():

    """
    delete geo by camera range also works with an animated camera
    """

    help(camUvDeleteAnim)

    import hou
    nodeSelect= hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))
    black=hou.Color ((0,0,0))

    for node in nodeSelect:
        parent = node.parent()
        parentString= parent.name()
        getName= node.name()
        connectNode = node.outputs()
        outNull = node.createOutputNode("null","inCamDeleteAnim")
        outNull.setPosition(node.position())
        outNull.move([0, -.75])
        outNull.setColor(black)
        #create left branch
        blackColor= outNull.createOutputNode("color","black")
        blackColor.move([-.75, -.75])
        blackColor.setParms({"colorr":0,"colorg":0,"colorb":0})
        #create right branch
        wrangleSnippet=outNull.createOutputNode("attribwrangle","camUvDelete")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
vector ndc=toNDC("/obj/root/transform/camera/cambaked/ppCam/ppCamShape",@P); // DONT FORGET TO FILL CAM PATH
@Cd = ndc; // viz
float secu = 0.1;
if(ndc.x+secu<0||ndc.x-secu>1||ndc.y+secu<0||ndc.y-secu>1||ndc.z>1){
removepoint(geoself(),@ptnum);
}"""}) 
        wrangleSnippet.move([0.75, -.75])
        redColor= wrangleSnippet.createOutputNode("color","red")
        redColor.move([0, -.35])
        redColor.setParms({"colorr":1,"colorg":0,"colorb":0}) 
        #create solver
        mysolver = blackColor.createOutputNode("solver","transferColor")
        solverName = mysolver.name()
        mysolver.move([0, -1.5]) 
        mysolver.setInput(1,redColor)
        mytransfert = hou.node('/obj/'+parentString+'/'+solverName+'/d/s').createNode('attribtransfer','transferUv')
        hou.node('/obj/'+parentString+'/'+solverName+'/d/s/transferUv').setInput(0,hou.node('/obj/'+parentString+'/'+solverName+'/d/s/Prev_Frame'))
        hou.node('/obj/'+parentString+'/'+solverName+'/d/s/transferUv').setInput(1,hou.node('/obj/'+parentString+'/'+solverName+'/d/s/Input_2'))
        mytransfert.setDisplayFlag(True) #set display flag true
        mytransfert.setParms({"thresholddist":0.1})
        time = mysolver.createOutputNode("timeshift","Fend")
        time.parm("frame").deleteAllKeyframes()
        time.setParms({"frame":240})
        
        removePointVex=time.createOutputNode("attribwrangle","deleteGeo")
        removePointVex.setColor(pink)
        removePointVex.setParms({"snippet":"""
if(@Cd.x<0.5)removepoint(0,@ptnum);
"""}) 
        removePointVex.setDisplayFlag(True)

    print("--- Don't forget to check the campath in camUvdelete ---")


def fillHoles ():

    '''
    add point between point if the distance between them is to big
    '''

    help(fillHoles)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","simpleFillHoles")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
float searchrad=ch("searchrad");
float mindist=ch("mindist");
int maxpoints=chi("maxpoints");
int fillpoints=chi("fillpts");

vector clpos;
int handle=pcopen(0,"P",@P,searchrad,maxpoints+1);
int i=0;
while(pciterate(handle))
{
    if (i==0) // the first point found should be the closest, in this case, itself. We want to skip it.
    {
        i++;
        continue;
    }
    pcimport(handle,"P",clpos);
    if (length(@P-clpos)>mindist)
    {
        vector pointstep=(clpos-@P)/(fillpoints*2+1); // this ensures there are no duplicate point
                                                     // at the cost of doubling the fill points number
        for (int t=0;t<fillpoints;t++)
            addpoint(0,@P+(pointstep*float(t+1)));
    }
}
"""}) 
    print("--- Don't forget to create the channel ---")


def pointDeleteByProximity ():

    '''
    if a point is to far from is neighbour then delete it
    '''
    
    help(pointDeleteByProximity)

    import hou
    nodeSelect = hou.selectedNodes()
    pink=hou.Color((0.98,0.275,0.275))

    for node in nodeSelect:
        wrangleSnippet=node.createOutputNode("attribwrangle","pointDeleteByProximity")
        wrangleSnippet.setColor(pink)
        wrangleSnippet.setParms({"snippet":"""
int numPoint = chi("numPoint");

int mypc = pcopen(0,"P",@P,chf("radius"),numPoint);

@Cd= chramp("ramp",fit(pcnumfound(mypc),0,numPoint,0,1));

if (@Cd.x<chf("seuilColor"))removepoint(0,@ptnum);
"""}) 
    
    print("--- Don't forget to create the channel ---")

def inputColor ():
    """
    set the color of inputs node to the color of the selected node
    """

    help(inputColor)

    import hou
    nodeSelect = hou.selectedNodes()
   
    for node in nodeSelect:
        inputNode = node.inputs()
        currentColor = node.color()
        for n in inputNode:
            n.setColor(currentColor)


def inputSelectNode ():

    """
    select all inputs node of the selected node
    usefull with a lot of merge node
    """

    help(inputSelectNode)

    import hou
    nodeSelect = hou.selectedNodes()
    
    for node in nodeSelect:
        inputNode = node.inputs()
        node.setSelected(False)
        for n in inputNode:
            n.setSelected(True)
    


def importAbcAsset ():
    
    """
    import all alembic file from $HIP/abc/ in a new sop call alembicImport
    """

    help(importAbcAsset)

    import hou
    import os
 
    
    #set path
    hipPath = hou.expandString('$HIP')
    path = hipPath + "/abc/"
    print (path)
    
    listPath = os.listdir(path)
    
    obj = hou.node("/obj")
    alembicImport= obj.createNode ("geo","alembicImport")
    
    file1 = hou.node("/obj/alembicImport/file1")
    file1.destroy()
  
    for n in listPath:
        print (n)
        currentFile=alembicImport.createNode("alembic",n)
        #set fileName
        currentFile.setParms({"fileName":"$"+"HIP/abc/"+n})

    #reload geo callback
    #prepa param
    parm_group = alembicImport.parmTemplateGroup()
    parm_folder = hou.FolderParmTemplate("folder","reload")
    #button run code
    button=hou.ButtonParmTemplate("reload","Reload")
    button.setTags({"script_callback_language":"python","script_callback":"import y \ny.reloadAlembic()"})
    parm_folder.addParmTemplate(button)
    #append param
    parm_group.append(parm_folder)
    alembicImport.setParmTemplateGroup(parm_group)

def reloadAlembic ():

    import hou
    import os
    alembicImport= hou.node("/obj/alembicImport")
    
    children = alembicImport.children()
    for n in children:
        n.destroy()
    
    #set path
    hipPath = hou.expandString('$HIP')
    path = hipPath + "/abc/"
    print (path)
    
    listPath = os.listdir(path)
    
    obj = hou.node("/obj")
    alembicImport= hou.node("/obj/alembicImport")
  
    for n in listPath :
        print (n)
        currentFile=alembicImport.createNode("alembic",n)
        #set fileName
        currentFile.setParms({"fileName":"$"+"HIP/abc/"+n})


def importGeoAsset ():
    
    """
    import all geo file from $HIP/geo/ in a new sop call geoImport
    """

    help(importGeoAsset)

    import hou
    import os
 
    
    #set path
    hipPath = hou.expandString('$HIP')
    path = hipPath + "/geo/"
    print (path)
    
    listPath = os.listdir(path)
    
    obj = hou.node("/obj")
    geoImport= obj.createNode ("geo","geoImport")

    file1 = hou.node("/obj/geoImport/file1")
    file1.destroy()
  
    for n in listPath :
        print (n)
        currentFile=geoImport.createNode("file",n)
        #set fileNames
        currentFile.setParms({"file":"$"+"HIP/geo/"+n})
    
    #reload geo callback
    #prepa param
    parm_group = geoImport.parmTemplateGroup()
    parm_folder = hou.FolderParmTemplate("folder","reload")
    #button run code
    button=hou.ButtonParmTemplate("reload","Reload")
    button.setTags({"script_callback_language":"python","script_callback":"import y \ny.reloadGeo()"})
    parm_folder.addParmTemplate(button)
    #append param
    parm_group.append(parm_folder)
    geoImport.setParmTemplateGroup(parm_group)


def reloadGeo ():

    import hou
    import os
    geoImport= hou.node("/obj/geoImport")
    
    children = geoImport.children()
    for n in children:
        n.destroy()
    
    #set path
    hipPath = hou.expandString('$HIP')
    path = hipPath + "/geo/"
    print (path)
    
    listPath = os.listdir(path)
    
    obj = hou.node("/obj")
    geoImport= hou.node("/obj/geoImport")
  
    for n in listPath :
        print (n)
        currentFile=geoImport.createNode("file",n)
        #set fileName
        currentFile.setParms({"file":"$"+"HIP/geo/"+n})

def exit():
    """
    change scene mode in manual, save, and exit 
    """
    help(exit)
    import hou
    
    mode = hou.updateModeSetting().name()
    if mode == 'AutoUpdate':
        hou.setUpdateMode(hou.updateMode.Manual)
    hou.hipFile.save(file_name=None, save_to_recent_files=True)
    hou.exit(exit_code=0, suppress_save_prompt=False)

def open():
    """change scene mode in manual, save, and open open windows"""

    help (open)

    import hou
    
    mode = hou.updateModeSetting().name()
    if mode == 'AutoUpdate':
        hou.setUpdateMode(hou.updateMode.Manual)
        
    hou.hipFile.save(file_name=None, save_to_recent_files=True)
    f=hou.ui.selectFile()
    hou.hipFile.load(f) 

def explorer():
    """open explorer at $HIP path"""
    help(explorer)
    
    import hou
    import os
    import platform
    import subprocess

    path = hou.expandString("$HIP")

    print(path)
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def fileMaker():
    """Create some basic folder at root $HIP"""
    import hou
    import os
    from os.path import exists

    path = hou.expandString("$HIP")
    structure = ["abc","geo","screenShot","cache","render","source","ref"]
    
    
    for n in structure:
        if exists(path + '/'+ n):
            continue
        else:
            dossiers = path + '/'+ n 
            os.makedirs(dossiers)
            print (dossiers)


def screenShot():
    """take a screen shot of the current viewport at the current frame"""
    help(screenShot)
    import hou
    import toolutils
    import os
    #selected node
    nodeSelect = hou.selectedNodes()
    path = hou.expandString("$HIP")
    frame = hou.expandString("$F")
    frame = int(frame)
    black=hou.Color((0,0,0))
    #name check there is a node selected 
    if len(nodeSelect)<1: 
        print ("!!!    error: select a node    !!!")
    else:
        for node in nodeSelect:
            name = node.name()
            node.setColor(black)
        #Get the current Desktop
        desktop = hou.ui.curDesktop()
        # Get the scene viewer
        scene= toolutils.sceneViewer()
        flipbook_options = scene.flipbookSettings().stash()
        # set frame range
        flipbook_options.frameRange((frame,frame)) 
        #set output path
        root ="{1}/{2}/{0}/".format(name,path,"screenShot")
        if os.path.exists(root):
            listPath = os.listdir(root)
            inc = len(listPath)
            inc = int(inc)   
            outputPath = "{}{}.{:04d}.jpg".format(root,name,inc)
        else:
            os.makedirs(root)
            inc = 0
            outputPath = "{}{}.{:04d}.jpg".format(root,name,inc)
        #set flipbook current path     
        flipbook_options.output(outputPath)
        #run flipbook
        scene.flipbook(scene.curViewport(),flipbook_options)
        # reload image
        print (outputPath)
        editor = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
        image = hou.NetworkImage() 
        image.setPath(outputPath)
        image.setRect(hou.BoundingRect(0, 0, 5, 5))
        image.setRelativeToPath(node.path())
        editor.setBackgroundImages([image])




        




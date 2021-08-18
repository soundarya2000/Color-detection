#Code for Color identification in images
import cv2                                           #opencv
import pandas as pd

img_path="color detection.jpg"                                 #path of image
csv_path="dataset.txt"                              #path of data set

csv=pd.read_csv(csv_path)                          #read the csv file

#Modifying CSV
index=['color','color_name','hex','R','G','B']       #adding header
csv=pd.read_csv(csv_path,names=index,header=None)
print(csv.head(10))                                 #display the first 10 rows
print("length:{}".format(len(csv)))                 #total no.of rows in data set
#Some intial conditions for later use
clicked=False
r=g=b=x_pos=y_pos=0

##Reading and modifying img
img=cv2.imread(img_path)
resize=cv2.resize(img,(1000,800))
print(img)                   #prints the img in the form of array of pixels as img is a collection of pixels.
print(resize)                                     # prints the resized image

#To get the color name by calculating the distance
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname
#To calculate the rgb values of the pixel which we double click.
def draw_function(event,x,y,flags,params):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global clicked,r,g,b,x_pos,y_pos
        clicked=True
        x_pos=x
        y_pos=y
        print("x and y coordinates:",x,y)  #Returns x and y position of the button clicked
        b,g,r=resize[y,x]      #in opencv, img will be in bgr format
        b=int(b)
        g=int(g)
        r=int(r)
        print("BGR value:",b,g,r)

cv2.namedWindow("Color Detection")
cv2.setMouseCallback("Color Detection",draw_function)
while True:

    cv2.imshow("Color Detection", resize)
    if clicked:

        # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(resize, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(resize, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(resize, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

        # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()

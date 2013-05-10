vid = videoinput('winvideo', 1, 'YUY2_1024x576');
src = getselectedsource(vid);

vid.FramesPerTrigger = 1;

preview(vid);

vid.ReturnedColorspace = 'rgb';

preview(vid);

start(vid);

stoppreview(vid);


imwrite(getdata(vid), 'C:\Users\Xueliang Liu\Desktop\48hours\finalfield61.jpg');


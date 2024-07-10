import cv2
import numpy as np
import mss
from crosshair_overlay import play_hit_sound, play_miss_sound, play_multi_hit_sound

def detect_kills(app):
    sct = mss.mss()
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}  # Adjust based on your screen resolution
    kill_feed_region = {"top": 50, "left": 1700, "width": 200, "height": 100}  # Region for the kill feed, adjust as needed

    hit_count = 0
    kill_order = ['kill1', 'kill2', 'kill3', 'kill4', 'kill5']
    
    while True:
        # Capture the screen
        screen_img = np.array(sct.grab(monitor))
        
        # Extract the kill feed region
        kill_feed_img = screen_img[kill_feed_region['top']:kill_feed_region['top'] + kill_feed_region['height'],
                                   kill_feed_region['left']:kill_feed_region['left'] + kill_feed_region['width']]

        # Split the kill feed region into left and right parts
        height, width, _ = kill_feed_img.shape
        left_img = kill_feed_img[:, :width // 2]
        right_img = kill_feed_img[:, width // 2:]

        # Convert to HSV for color detection
        hsv_left = cv2.cvtColor(left_img, cv2.COLOR_BGR2HSV)
        hsv_right = cv2.cvtColor(right_img, cv2.COLOR_BGR2HSV)

        # Define color ranges for yellow and red (adjust as needed)
        yellow_lower = np.array([20, 100, 100])
        yellow_upper = np.array([30, 255, 255])
        red_lower1 = np.array([0, 100, 100])
        red_upper1 = np.array([10, 255, 255])
        red_lower2 = np.array([160, 100, 100])
        red_upper2 = np.array([179, 255, 255])

        # Create masks for yellow and red
        yellow_mask = cv2.inRange(hsv_left, yellow_lower, yellow_upper)
        red_mask1 = cv2.inRange(hsv_right, red_lower1, red_upper1)
        red_mask2 = cv2.inRange(hsv_right, red_lower2, red_upper2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        # Check if there are significant yellow and red regions in the left and right parts respectively
        yellow_count = cv2.countNonZero(yellow_mask)
        red_count = cv2.countNonZero(red_mask)

        if yellow_count > 500 and red_count > 500:  # Adjust the threshold based on your screen area and changes
            hit_count += 1
            play_hit_sound()
            if hit_count == 5:
                play_multi_hit_sound()
                app.change_crosshair('kill5')
                hit_count = 0
            else:
                app.change_crosshair(kill_order[hit_count - 1])
        else:
            play_miss_sound()
            app.change_crosshair('miss')
            hit_count = 0

        app.root.update_idletasks()
        app.root.update()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

import cv2
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import numpy as np

def md(input_path, output_path):
    # Load image and convert to grayscale
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to binarize image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply morphological operations to remove noise and fill gaps
    kernel = np.ones((3,3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)

    # Apply topological skeletonization to get skeleton image
    skeleton = cv2.ximgproc.thinning(morph)

    # Detect ridge bifurcations and endings using skeleton image
    bifurcation_points = []
    ending_points = []
    rows, cols = skeleton.shape
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if skeleton[i][j] != 0:
                window = skeleton[i-1:i+2, j-1:j+2]
                count = cv2.countNonZero(window)
                if count == 2:
                    bifurcation_points.append((j, i))
                elif count == 1:
                    ending_points.append((j, i))

    # Display original image with detected points
    fig, ax = plt.subplots()
    ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    for point in bifurcation_points:
        ax.plot(point[0], point[1], 'go', markersize=5)
        ax.annotate(f"({point[0]},{point[1]})", (point[0], point[1]), textcoords="offset points", xytext=(5,5), ha='left', va='bottom', fontsize=6)
    for point in ending_points:
        ax.plot(point[0], point[1], 'ro', markersize=5)
        ax.annotate(f"({point[0]},{point[1]})", (point[0], point[1]), textcoords="offset points", xytext=(5,5), ha='left', va='bottom', fontsize=6)

    minutiae_count = len(bifurcation_points+ending_points)

    # Add axes coordinates
    ax.set_xlim(0, cols)
    ax.set_ylim(rows, 0)
    ax.set_xticks(range(0, cols, 100))
    ax.set_yticks(range(0, rows, 100))
    ax.set_xlabel("X-axis (pixels)")
    ax.set_ylabel("Y-axis (pixels)")

    # Save image to output directory
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    return minutiae_count
    #plt.close(fig)

#--------------------------------------------------------------------------#
#generate prime numbers
def is_prime(minutiae_count):
    #Returns True if n is a prime number, False otherwise.
    if minutiae_count < 2:
        return False
    for i in range(2, int(minutiae_count ** 0.5) + 1):
        if minutiae_count % i == 0:
            return False
    return True

def get_nearest_primes(minutiae_count):
    #Returns the two nearest prime numbers before and after n.
    # Find the nearest prime number before n
    prime_before = None
    for i in range(minutiae_count - 1, 1, -1):
        if is_prime(i):
            prime_before = i
            break
    
    # Find the nearest prime number after n
    prime_after = None
    i = minutiae_count + 1
    while True:
        if is_prime(i):
            prime_after = i
            break
        i += 1
    
    return prime_before, prime_after

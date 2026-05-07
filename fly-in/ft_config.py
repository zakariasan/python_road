from models import Zone

WIDTH, HEIGHT = 1920, 961
PADDING = 100
NODE_RADIUS = 30
BORDER_WIDTH = 5
RECT_SIZE = 28
ZONE_COLORS = {
    Zone.normal: (200, 200, 255),
    Zone.blocked: (100, 100, 100),
    Zone.restricted: (255, 100, 100),
    Zone.priority: (100, 255, 100),
}
BORDER_COLORS = {
    Zone.normal: (100, 100, 255),
    Zone.blocked: (255, 0, 0),
    Zone.restricted: (125, 0, 0),
    Zone.priority: (200, 155, 200),
}
START_COLOR = (0, 255, 0)
END_COLOR = (255, 255, 0)

# bms-kps-py
 BMS Keys per second py

```json5
{
    "window": {     // Window data
        "x": 400,   // Width
        "y": 250    // Height
    },
    "keys": [
        /*
         * Key data
         * [0] = Controller key number
         * [1] = Key type
         * [2] = Position X
         * [3] = Position Y
         * [4] = Width, Radius if circle
         * [5] = Height, null if circle
         * [6] = Key color 0-255
         */
        [0, 0, 100, 125, 50, 90, 255],
        [1, 0, 133, 25, 50, 90, 0],
        [2, 0, 165, 125, 50, 90, 255],
        [3, 0, 198, 25, 50, 90, 0],
        [4, 0, 230, 125, 50, 90, 255],
        [5, 0, 263, 25, 50, 90, 0],
        [6, 0, 295, 125, 50, 90, 255]
    ],
    "kps": { // Keys per second setting
        "enabled": true,
        "x": 5,
        "y": 5,
        "font": "dist/Roboto-Black.ttf",
        "size": 30
    },
    "joystick_id": 0 // Joystick connected ID
}
```
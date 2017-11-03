game.resources = [
    /**
     * Graphics.
     */
    // the main player spritesheet
    { name: "gripe_run_right", type: "image", src: static_url + "jackit/data/img/sprite/gripe_run_right.png" },
    // the spinning coin spritesheet
    { name: "spinning_coin_gold", type: "image", src: static_url + "jackit/data/img/sprite/spinning_coin_gold.png" },
    // our enemty entity
    { name: "wheelie_right", type: "image", src: static_url + "jackit/data/img/sprite/wheelie_right.png" },
    // game font
    { name: "PressStart2P", type: "image", src: static_url + "jackit/data/fnt/PressStart2P.png" },
    { name: "PressStart2P", type: "binary", src: static_url + "jackit/data/fnt/PressStart2P.fnt" },
    // title screen
    { name: "title_screen", type: "image", src: static_url + "jackit/data/img/gui/title_screen.png" },
    // the parallax background
    { name: "area01_bkg0", type: "image", src: static_url + "jackit/data/img/area01_bkg0.png" },
    { name: "area01_bkg1", type: "image", src: static_url + "jackit/data/img/area01_bkg1.png" },
    // our level tileset
    { name: "area01_level_tiles", type: "image", src: static_url + "jackit/data/img/map/area01_level_tiles.png" },

    /*
     * Maps.
     */
    { name: "level01", type: "tmx", src: static_url + "jackit/data/map/level01.tmx" },
    //{ name: "level02", type: "tmx", src: static_url + "jackit/data/map/level02.tmx" },

    /*
     * Background music.
     */
    { name: "dst-inertexponent", type: "audio", src: static_url + "jackit/data/bgm/" },

    /*
     * Sound effects.
     */
    { name: "cling", type: "audio", src: static_url + "jackit/data/sfx/" },
    { name: "stomp", type: "audio", src: static_url + "jackit/data/sfx/" },
    { name: "jump", type: "audio", src: static_url + "jackit/data/sfx/" }
];

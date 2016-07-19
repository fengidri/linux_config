--
-- author       :   丁雪峰
-- time         :   2016-07-16 15:22:45
-- email        :   fengidri@yeah.net
-- version      :   1.0.1
-- description  :
--


local _M = {}
local awful = require("awful")

-- Table of layouts to cover with awful.layout.inc, order matters.
_M.layouts =
{
    awful.layout.suit.floating,
    awful.layout.suit.tile,
    awful.layout.suit.tile.left,
    awful.layout.suit.tile.bottom,
    awful.layout.suit.tile.top,
    awful.layout.suit.fair,
    awful.layout.suit.fair.horizontal,
    awful.layout.suit.spiral,
    awful.layout.suit.spiral.dwindle,
    awful.layout.suit.max,
    awful.layout.suit.max.fullscreen,
    awful.layout.suit.magnifier
}

_M.right_widgets = {}

return _M

--
-- author       :   丁雪峰
-- time         :   2016-07-16 15:29:17
-- email        :   fengidri@yeah.net
-- version      :   1.0.1
-- description  :
--

local awful = require("awful")
local vars = require("vars")
-- Theme handling library
local beautiful = require("beautiful")

local myawesomemenu = {
   { "restart", awesome.restart },
   { "quit", awesome.quit }
}

local mymainmenu = awful.menu({ items = { { "awesome", myawesomemenu, beautiful.awesome_icon },
                                    { "open terminal", 'xterm' },
                                    { "chromium", "chromium" },
                                    { "gvim", "gvim" },
                                  }
                        })
vars.mainmenu = mymainmenu

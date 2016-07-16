--
-- author       :   丁雪峰
-- time         :   2016-07-16 15:29:17
-- email        :   fengidri@yeah.net
-- version      :   1.0.1
-- description  :
--

local awful = require("awful")
local myawesomemenu = {
   { "manual", terminal .. " -e man awesome" },
   { "edit config", editor_cmd .. " " .. awesome.conffile },
   { "restart", awesome.restart },
   { "quit", awesome.quit }
}

mymainmenu = awful.menu({ items = { { "awesome", myawesomemenu, beautiful.awesome_icon },
                                    { "open terminal", terminal },
                                    { "chromium", "chromium" },
                                    { "gvim", "gvim" },
                                  }
                        })

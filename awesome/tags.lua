--
-- author       :   丁雪峰
-- time         :   2016-07-16 15:19:05
-- email        :   fengidri@yeah.net
-- version      :   1.0.1
-- description  :
--
local vars = require('vars')
local awful = require("awful")

tags = {}
for s = 1, screen.count() do
    -- Each screen has its own tag table.
    tags[s] = awful.tag({ 'Web', "Code", "Doc", "O1", "O2"}, s, vars.layouts[1])
end
return tags

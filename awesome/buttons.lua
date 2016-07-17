--
-- author       :   丁雪峰
-- time         :   2016-07-17 00:38:22
-- email        :   fengidri@yeah.net
-- version      :   1.0.1
-- description  :
--

local awful = require("awful")
local vars = require("vars")
local buttons = {}

local modkey = "Mod4"

buttons.taglist = awful.util.table.join(
                    awful.button({ }, 1, awful.tag.viewonly),
                    awful.button({ modkey }, 1, awful.client.movetotag),
                    awful.button({ }, 3, awful.tag.viewtoggle),
                    awful.button({ modkey }, 3, awful.client.toggletag),
                    awful.button({ }, 4, function(t) awful.tag.viewnext(awful.tag.getscreen(t)) end),
                    awful.button({ }, 5, function(t) awful.tag.viewprev(awful.tag.getscreen(t)) end),
                    awful.button({ }, 9, function(t) awful.tag.viewnext(awful.tag.getscreen(t)) end),
                    awful.button({ }, 10, function(t) awful.tag.viewprev(awful.tag.getscreen(t)) end)
                    )

buttons.tasklist = awful.util.table.join(
                     awful.button({ }, 1, function (c)
                                              if c == client.focus then
                                                  c.minimized = true
                                              else
                                                  -- Without this, the following
                                                  -- :isvisible() makes no sense
                                                  c.minimized = false
                                                  if not c:isvisible() then
                                                      awful.tag.viewonly(c:tags()[1])
                                                  end
                                                  -- This will also un-minimize
                                                  -- the client, if needed
                                                  client.focus = c
                                                  c:raise()
                                              end
                                          end),
                     awful.button({ }, 3, function ()
                                              if instance then
                                                  instance:hide()
                                                  instance = nil
                                              else
                                                  instance = awful.menu.clients({
                                                      theme = { width = 250 }
                                                  })
                                              end
                                          end),
                     awful.button({ }, 4, function ()
                                              awful.client.focus.byidx(1)
                                              if client.focus then client.focus:raise() end
                                          end),
                     awful.button({ }, 5, function ()
                                              awful.client.focus.byidx(-1)
                                              if client.focus then client.focus:raise() end
                                          end))

buttons.client = awful.util.table.join(
    awful.button({ }, 1, function (c) client.focus = c; c:raise() end),
    awful.button({ modkey }, 1, awful.mouse.client.move),
    awful.button({ modkey }, 3, awful.mouse.client.resize),
    awful.button({ }, 9, function(t) awful.tag.viewnext(awful.tag.getscreen(t)) end),
    awful.button({ }, 10, function(t) awful.tag.viewprev(awful.tag.getscreen(t)) end)
    )

root.buttons(awful.util.table.join(
    awful.button({ }, 3, function () vars.mainmenu:toggle() end),
    awful.button({ }, 4, awful.tag.viewnext),
    awful.button({ }, 5, awful.tag.viewprev),
    awful.button({ }, 9, awful.tag.viewnext),
    awful.button({ }, 10, awful.tag.viewprev)
))
return buttons


--
-- author       :   丁雪峰
-- time         :   2016-07-17 00:52:49
-- email        :   fengidri@yeah.net
-- version      :   1.0.1
-- description  :
--

local awful = require("awful")
local beautiful = require("beautiful")

local buttons = require("buttons")
local keys = require('keys')

-- {{{ Rules
-- Rules to apply to new clients (through the "manage" signal).
awful.rules.rules = {
    -- All clients will match this rule.
    { rule = { },
    properties = { border_width = beautiful.border_width,
    border_color = beautiful.border_normal,
    focus = awful.client.focus.filter,
    raise = true,
    keys = keys.client,
    buttons = buttons.client
} },
    { rule = { class = "MPlayer" },
    properties = { floating = true } },
    { rule = { class = "pinentry" },
    properties = { floating = true } },
    { rule = { class = "gimp" },
    properties = { floating = true } },

    {
        rule_any = {
            instance = {'TM.exe', 'QQ.exe'},
        },
        properties = {
            -- This, together with myfocus_filter, make the popup menus flicker taskbars less
            -- Non-focusable menus may cause TM2013preview1 to not highlight menu
            -- items on hover and crash.
            focusable = true,
            floating = true,
            -- 去掉边框
            border_width = 0,
        }
    },

    -- Set Firefox to always map on tags number 2 of screen 1.
    -- { rule = { class = "Firefox" },
    --   properties = { tag = tags[1][2] } },
}
-- }}}

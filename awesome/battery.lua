--
-- author       :   丁雪峰
-- time         :   2016-07-16 15:32:38
-- email        :   fengidri@yeah.net
-- version      :   1.0.1
-- description  :
--

-- battery warning
local awful = require("awful")
local vars = require("vars")
local wibox = require("wibox")

local function trim(s)
  return s:find'^%s*$' and '' or s:match'^%s*(.*%S)'
end

local mybattmon = wibox.widget.textbox()

local function bat_notification()
  local f_capacity = assert(io.open("/sys/class/power_supply/BAT0/capacity", "r"))
  local f_status = assert(io.open("/sys/class/power_supply/BAT0/status", "r"))
  local bat_capacity = tonumber(f_capacity:read("*all"))
  local bat_status = trim(f_status:read("*all"))

  if (bat_capacity <= 10 and bat_status == "Discharging") then
    naughty.notify({ title      = "Battery Warning"
      , text       = "Battery low! " .. bat_capacity .."%" .. " left!"
      , fg="#ffffff"
      , bg="#C91C1C"
      , timeout    = 15
      , position   = "bottom_right"
    })
  end

  mybattmon:set_text(" Battery:" .. bat_capacity .. "% ")
end

battimer = timer({timeout = 60})
battimer:connect_signal("timeout", bat_notification)
battimer:start()


-- the widget

table.insert(vars.right_widgets, mybattmon)

-- TODO: NOTIFY MAKES A BOX< BUT IG DOESN"T MAKE IT LARGER WHEN NEW NOTIFICATIONS COME IN

local win_

local function notify_output(command, opts)
  local output = ""
  local notification
  local notify = function(msg, level)
    local notify_opts = vim.tbl_extend(
      "keep",
      opts or {},
      {
        title = table.concat(command, " "),
        replace = notification,
      }
    )
    notification = vim.notify(msg, level, notify_opts)
    if win_ ~= nil then
      local buf = vim.api.nvim_win_get_buf(win_)
      vim.api.nvim_buf_set_option(buf, "filetype", "markdown")
    end
  end

  local on_out = function(_, data)
    local data_str = table.concat(data, "\n")
    if #data_str == 0 then return end
    output = output .. data_str
    notify(output, "info")
  end

  local on_err = function(_, data)
    local data_str = table.concat(data, "\n")
    if #data_str == 0 then return end
    output = output .. data_str
    notify(output, "error")
  end

  vim.fn.jobstart(command, {
    on_stdout = on_out,
    on_stderr = on_err,
    on_exit = function(_, code)
      if #output == 0 then
        notify("No output of command, exit code: " .. code, "warn")
      end
    end,
  })
end

local function CFSubmit()
  local source_file_path = vim.fn.expand("%:p")
  local submitter = "/home/aks/Tools/codeforces_submitter_vim/plugin/submitter.py"
  notify_output({ submitter, source_file_path }, {
    title = "CFSubmit",
    -- timeout = 3000,
    on_open = function(wind)
      win_ = wind
      vim.api.nvim_win_set_height(wind, 5)
      local buf = vim.api.nvim_win_get_buf(wind)
      vim.api.nvim_buf_set_option(buf, "filetype", "markdown")
    end
  })
end

local function CFLastVerdict()
  local checker_file = "/home/aks/Tools/codeforces_submitter_vim/plugin/checker.py"
  notify_output({ "python3", checker_file }, {
    title = "Last Verdict",
    -- timeout = 3000,
    on_open = function(wind)
      win_ = wind
      vim.api.nvim_win_set_height(wind, 8)
      local buf = vim.api.nvim_win_get_buf(wind)
      vim.api.nvim_buf_set_option(buf, "filetype", "markdown")
    end
  })
end

vim.api.nvim_create_user_command("CodeForceSubmit", CFSubmit, {})
vim.api.nvim_create_user_command("LastVerdict", CFLastVerdict, {})

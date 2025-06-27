import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GSheetLogger:
    def __init__(self, creds_path, sheet_name, user_email):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        # create and share
        self.sheet = client.create(sheet_name)
        self.sheet.share(user_email, perm_type='user', role='writer')
        # only two worksheets:- TradeLog and Summary
        for ws in self.sheet.worksheets():
            if ws.title!='TradeLog':
                self.sheet.add_worksheet('TradeLog', rows=1000, cols=10)
                self.sheet.del_worksheet(ws)
        self.sheet.add_worksheet('Summary', rows=1000, cols=5)

    # def log_to_sheets(self, stocks_results):
    #     tl = self.sheet.worksheet('TradeLog')
    #     sm = self.sheet.worksheet('Summary')
    #     tl.clear()
    #     sm.clear()

    #     # TradeLog
    #     row = 1
    #     for ticker, trades_df, summary in stocks_results:
    #         tl.update_cell(row, 1, ticker)
    #         row += 1

    #         if not trades_df.empty:
    #             # header
    #             tl.insert_row(list(trades_df.columns), row)
    #             row += 1
    #             # format dates
    #             df = trades_df.copy()
    #             df['entry_date'] = df['entry_date'].dt.strftime('%Y-%m-%d')
    #             df['exit_date']  = df['exit_date'].dt.strftime('%Y-%m-%d')
    #             for _, data_row in df.iterrows():
    #                 tl.insert_row(data_row.tolist(), row)
    #                 row += 1
    #         row += 1

    #     # Summary
    #     row = 1
    #     for ticker, trades_df, summary in stocks_results:
    #         sm.update_cell(row, 1, ticker)
    #         row += 1
    #         for k, v in summary.items():
    #             sm.update_cell(row, 1, k)
    #             sm.update_cell(row, 2, v)
    #             row += 1
    #         row += 1

    #     return self.sheet
    def log_to_sheets(self, stocks_results):
        tl = self.sheet.worksheet('TradeLog')
        sm = self.sheet.worksheet('Summary')
        tl.clear()
        sm.clear()

        # TradeLog
        row = 1
        for ticker, trades_df, summary in stocks_results:
            tl.update_cell(row, 1, ticker)
            row += 1

            if not trades_df.empty:
                # header row
                tl.insert_row(list(trades_df.columns), row)
                row += 1

                # format dates
                df = trades_df.copy()
                df['entry_date'] = df['entry_date'].dt.strftime('%Y-%m-%d')
                df['exit_date']  = df['exit_date'].dt.strftime('%Y-%m-%d')

                for _, data_row in df.iterrows():
                    # convert any numpy types to Python native
                    row_values = [x.item() if hasattr(x, 'item') else x for x in data_row.tolist()]
                    tl.insert_row(row_values, row)
                    row += 1
            row += 1

        # Summary sheet
        row = 1
        for ticker, trades_df, summary in stocks_results:
            sm.update_cell(row, 1, ticker)
            row += 1
            for k, v in summary.items():
                sm.update_cell(row, 1, str(k))
                # ensure v is JSON serializable
                val = v.item() if hasattr(v, 'item') else v
                sm.update_cell(row, 2, str(val))
                row += 1
            row += 1

        return self.sheet
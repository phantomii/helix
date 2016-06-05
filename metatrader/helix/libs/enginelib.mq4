//+------------------------------------------------------------------+
//|         Copyright 2015, S.Y.N.A.P.S.E Technology (Eugene Frolov) |
//|                                      http://helix.synapse.net.ru |
//+------------------------------------------------------------------+

//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.


class FileController {
	private:
		// Consts
		string API_TICK_FOLDER;
		string API_TICK_INSTRUMENT_FOLDER;

		int m_op_count;
		bool m_async_mode;
	public:
		// File status
		string FILE_STATUS_CREATING;
		string FILE_STATUS_CREATED;
		string FILE_STATUS_PROCESSING;
		string FILE_STATUS_DONE;
		string FILE_STATUS_ASYNC;

		FileController () {
			FILE_STATUS_CREATING = "creating";
			FILE_STATUS_CREATED = "created";
			FILE_STATUS_PROCESSING = "processing";
			FILE_STATUS_DONE = "done";
			FILE_STATUS_ASYNC = "async";

			m_op_count = 0;
		}
		
		bool init (const string instrument, const string api_path,
			       const bool async_mode) {
			// Create main folder
			if (!FolderCreate(api_path)) {
				PrintFormat("Failed to create folder %s. Error code %d",
					        api_path, GetLastError());
				return false;
			}

			// Create API folde
			API_TICK_FOLDER = StringConcatenate(api_path, "/tick/");
			if (!FolderCreate(API_TICK_FOLDER)) {
				PrintFormat("Failed to create folder %s. Error code %d",
					        API_TICK_FOLDER, GetLastError());
				return false;
			}

			// Create INSTRUMENT folder
			API_TICK_INSTRUMENT_FOLDER = StringConcatenate(API_TICK_FOLDER,
				                                           instrument);
			if (!FolderCreate(API_TICK_INSTRUMENT_FOLDER)) {
				PrintFormat("Failed to create folder %s. Error code %d",
					        API_TICK_INSTRUMENT_FOLDER, GetLastError());
				return false;
			}

			m_async_mode = async_mode;
			return true;
		};

		string get_file_name() {
			m_op_count += 1;
			return StringFormat("%d", m_op_count);
		}

		string get_new_filepath() {
			string result = StringConcatenate(API_TICK_INSTRUMENT_FOLDER, "/",
				                              get_file_name(), ".");
			if (m_async_mode) {
				result = StringConcatenate(result, FILE_STATUS_CREATING);
			} else {
				result = StringConcatenate(result, FILE_STATUS_ASYNC);
			}
			return result;
		};

		string change_status (const string file_path, const string new_status) {
			
			if (m_async_mode) {
				return file_path;
			}
			
			string result[];
			ushort sep = StringGetCharacter(".", 0);
			int substring_count = StringSplit(file_path, sep, result);
			if (substring_count != 2) {
				PrintFormat("Failed to split filename %s.", file_path);
				return "";
			}
			string new_file_path = StringConcatenate(result[0], ".", new_status);
			if (FileMove(file_path, 0, new_file_path, FILE_REWRITE) == false) {
				PrintFormat("Can't rename file %s. Error code %d",
					        file_path, GetLastError());
				return "";
			}
			return new_file_path;
		};

		bool wait_processing(const string file_path) {
			return true;
		}

		bool process_tick (const double ask, const double bid) {
			string file_path = get_new_filepath();
			int fd = FileOpen(file_path, FILE_WRITE|FILE_READ|FILE_CSV, "\t");
			if (fd == INVALID_HANDLE) {
				PrintFormat("Failed to open file %s. Error code %d",
					        file_path, GetLastError());
				return false;
			};
			if (FileWrite(fd, ask, bid) == 0) {
				PrintFormat("Failed to write file %s. Error code %d",
					        file_path, GetLastError());
				FileClose(fd);
				FileDelete(file_path);
				return false;
			};
			FileClose(fd);
			string result = change_status(file_path, FILE_STATUS_CREATED);
			if ( result == "") {
				PrintFormat("Failed to change file status to %s. Error code %d",
					        FILE_STATUS_CREATED, GetLastError());
				FileDelete(file_path);
				return false;
			}
			file_path = result;
			
			if (wait_processing(file_path) == false) {
				PrintFormat("Failed processing file %s. Error code %d",
					        file_path, GetLastError());
				FileDelete(file_path);
				return false;
			}

        	return true;
		};
};


class FileEngine {
	private:
		FileController m_file_controller;

	public:
		FileEngine () {};

		bool init (const string instrument, const string api_path,
			       const bool async_mode) {
			return m_file_controller.init(instrument, api_path, async_mode);
		};

		bool onTick(const double ask, const double bid) {
			return m_file_controller.process_tick(ask, bid);
		}
};

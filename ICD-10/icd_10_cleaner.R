library(tidyverse)
library(readxl)
library(writexl)
library(stringr)
library(zeallot)
library(odbc)
library(DBI)


valid_codes = read_csv('codes.txt')$code


# Function to process ICD-10 codes
icd_clean <- function(data, columns){
  
  # Identify non-matches
  #non_matches <- filter(data, !Code %in% valid_codes)
  df = data
  og = data
  non_matches = data.frame("case_number"=integer(),"column"=character(),"original"=character(),"cleaned"=character())
  deleted_codes = c()
  og_non_matches = data.frame("case_number"=integer(),"column"=character(),"code"=character())
  
  
  # For each ICD-10 column
  for (c in columns){
    # For each row
    for (row in 1:nrow(df)){
      
      df[row, c] = trimws(df[row, c])
      code = df[row, c]
      
      # Place codes
      if (c == "place_code"){
        if (str_length(df[row, c]) > 1 | !df[row, c] %in% seq(0,9)){
          # Keep only the single digit codes
          df[row, c] = NA
        }
      }
      
      # Activity codes
      else if (c == "activity_code"){
        if (str_length(df[row, c]) > 1 | !df[row, c] %in% c(0,1,2,3,4,8,9)){
          # Keep only the single digit codes
          df[row, c] = NA
        }
      }
      
      # For all other columns
      else {
        df[row, c] = toupper(df[row, c])
        
        # If code not valid
        if (!is.na(df[row, c]) & !df[row, c] %in% valid_codes){
          
          og_non_matches[nrow(og_non_matches)+1,] = c(df[row,"case_number"], c, df[row,c])
          
          # If last character is a letter, remove it
          if (length(grep("[A-Z]", str_sub(df[row, c], -1, -1)))==1){
            code = str_sub(df[row, c], 1, -2)
          }
          
          # If code has 4+ digits
          else if (str_length(code) > 3){
            
            # If code is missing decimal after 3rd character
            if (!str_detect(code, "\\.")){
              # Add decimal after 3rd character
              code <- paste0(str_sub(code, 1, 3), ".", str_sub(code, 4, -1))
            }
          }
          
          # # If first character is not a letter, delete code
          # else if (length(grep("[A-Z]", substr(code, 1, 1)))==0){
          #   deleted_codes = append(deleted_codes, df[row, c])
          #   df[row, c] <- NA
          # }
        }
        
        # Start check again    
        if (!is.na(code) & !code %in% valid_codes){
          # If code has more than 5 characters (including the decimal)
          if (str_length(code) > 5){
            code = substr(code, 1, 5)
          }
        }
        
        # If still not a valid code
        if (!is.na(code) & !code %in% valid_codes){
          # Pull back to 3 characters
          code <- str_sub(df[row, c], 1, 3)
        }
        
        df[row, c] = code
        
        
        # # Delete remaining codes that have only 2 characters
        # if (str_length(df[row, c]) == 2 & !is.na(df[row, c])){
        #   df[row, c] <- as.character(NA)
        # }
        
        # Pull invalid codes
        # If code not valid
        if (!is.na(code) & !code %in% valid_codes){
          # Add to non_matches
          non_matches[nrow(non_matches)+1,] = c(df[row,"case_number"], c, og[row,c], code)
          df[row, c] = NA
        }
      }
      
    }
  }
  
  #return(list(df, non_matches))
  return(df)
}

#-----------------------------------------------------------------------------
# Execute
#Import data
CDR_query <- read_file("C:\\Users\\jagvan\\OneDrive - South Australia Government\\Code\\SQL Server Management Studio\\Queries\\REDCap\\icd10.sql")
con <- dbConnect(odbc(), "CDR-DSN")
data <- dbGetQuery(con, CDR_query)
cols = colnames(data[-1:-3])

#Clean the data
data_cleaned <- icd_clean(data, cols)

#-----------------------------------------------------------------------------

#write_csv(data_cleaned, "icd_cleaned_190522.csv", na = "")
write_delim(data_cleaned, "icd_cleaned_120722.csv", na = "", delim = "|")


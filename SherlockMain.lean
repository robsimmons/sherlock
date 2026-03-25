import VersoManual
import Sherlock

def config : Verso.Genre.Manual.RenderConfig where
  emitTeX := false
  emitHtmlSingle := .no
  emitHtmlMulti := .immediately
  rootTocDepth := .some 2
  htmlDepth := 2

def main := Verso.Genre.Manual.manualMain (%doc Sherlock) (config := config)
